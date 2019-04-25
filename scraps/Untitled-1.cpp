#include <algorithm>
#include <map>
#include <utility>
#include <vector>

#include "caffe/layers/multibox_loss_layer.hpp"
#include "caffe/util/math_functions.hpp"

namespace caffe
{

/*
 *
    bottom: "mbox_loc"
    bottom: "mbox_conf"
    bottom: "mbox_priorbox"
    bottom: "label"
    top: "mbox_loss"
 *
 *
 */

template <typename Dtype>
void MultiBoxLossLayer<Dtype>::LayerSetUp(const vector<Blob<Dtype>*>& bottom,const vector<Blob<Dtype>*>& top)
{
  LossLayer<Dtype>::LayerSetUp(bottom, top);
  if (this->layer_param_.propagate_down_size() == 0)
  {
    this->layer_param_.add_propagate_down(true);
    this->layer_param_.add_propagate_down(true);
    this->layer_param_.add_propagate_down(false);
    this->layer_param_.add_propagate_down(false);
  }
  const MultiBoxLossParameter& multibox_loss_param =
      this->layer_param_.multibox_loss_param();
  multibox_loss_param_ = this->layer_param_.multibox_loss_param();

  num_ = bottom[0]->num();
  num_priors_ = bottom[2]->height() / 4; // 每幅图像中priorbox的数量
  // Get other parameters.
  CHECK(multibox_loss_param.has_num_classes()) << "Must provide num_classes.";
  num_classes_ = multibox_loss_param.num_classes(); // 类别数
  CHECK_GE(num_classes_, 1) << "num_classes should not be less than 1.";
  share_location_ = multibox_loss_param.share_location();// true
  loc_classes_ = share_location_ ? 1 : num_classes_; // 1
  background_label_id_ = multibox_loss_param.background_label_id(); // 0
  use_difficult_gt_ = multibox_loss_param.use_difficult_gt(); // true
  mining_type_ = multibox_loss_param.mining_type();// 默认为MAX_NEGATIVE
  if (multibox_loss_param.has_do_neg_mining()) // true
  {
    LOG(WARNING) << "do_neg_mining is deprecated, use mining_type instead.";
    do_neg_mining_ = multibox_loss_param.do_neg_mining();
    CHECK_EQ(do_neg_mining_,
             mining_type_ != MultiBoxLossParameter_MiningType_NONE);
  }
  do_neg_mining_ = mining_type_ != MultiBoxLossParameter_MiningType_NONE; // true

  if (!this->layer_param_.loss_param().has_normalization() &&
      this->layer_param_.loss_param().has_normalize())
  {
    normalization_ = this->layer_param_.loss_param().normalize() ?
                     LossParameter_NormalizationMode_VALID :
                     LossParameter_NormalizationMode_BATCH_SIZE;
  }
  else
  {
    normalization_ = this->layer_param_.loss_param().normalization();
  }

  if (do_neg_mining_) {
    CHECK(share_location_)
        << "Currently only support negative mining if share_location is true.";
  }

  vector<int> loss_shape(1, 1);
  // Set up localization loss layer.
  loc_weight_ = multibox_loss_param.loc_weight(); // 1.0
  loc_loss_type_ = multibox_loss_param.loc_loss_type();// SMOOTH_L1
  // fake shape.
  vector<int> loc_shape(1, 1);
  loc_shape.push_back(4);
  loc_pred_.Reshape(loc_shape);
  loc_gt_.Reshape(loc_shape);
  loc_bottom_vec_.push_back(&loc_pred_);
  loc_bottom_vec_.push_back(&loc_gt_);
  loc_loss_.Reshape(loss_shape);
  loc_top_vec_.push_back(&loc_loss_);
  if (loc_loss_type_ == MultiBoxLossParameter_LocLossType_L2)
  {
    LayerParameter layer_param;
    layer_param.set_name(this->layer_param_.name() + "_l2_loc");
    layer_param.set_type("EuclideanLoss");
    layer_param.add_loss_weight(loc_weight_);
    loc_loss_layer_ = LayerRegistry<Dtype>::CreateLayer(layer_param);
    loc_loss_layer_->SetUp(loc_bottom_vec_, loc_top_vec_);
  } else if (loc_loss_type_ == MultiBoxLossParameter_LocLossType_SMOOTH_L1) {
    LayerParameter layer_param;
    layer_param.set_name(this->layer_param_.name() + "_smooth_L1_loc");
    layer_param.set_type("SmoothL1Loss");
    layer_param.add_loss_weight(loc_weight_);
    loc_loss_layer_ = LayerRegistry<Dtype>::CreateLayer(layer_param);
    loc_loss_layer_->SetUp(loc_bottom_vec_, loc_top_vec_);
  } else {
    LOG(FATAL) << "Unknown localization loss type.";
  }
  // Set up confidence loss layer.
  conf_loss_type_ = multibox_loss_param.conf_loss_type();
  conf_bottom_vec_.push_back(&conf_pred_);
  conf_bottom_vec_.push_back(&conf_gt_);
  conf_loss_.Reshape(loss_shape);
  conf_top_vec_.push_back(&conf_loss_);
  if (conf_loss_type_ == MultiBoxLossParameter_ConfLossType_SOFTMAX)
  {
    CHECK_GE(background_label_id_, 0)
        << "background_label_id should be within [0, num_classes) for Softmax.";
    CHECK_LT(background_label_id_, num_classes_)
        << "background_label_id should be within [0, num_classes) for Softmax.";
    LayerParameter layer_param;
    layer_param.set_name(this->layer_param_.name() + "_softmax_conf");
    layer_param.set_type("SoftmaxWithLoss");
    layer_param.add_loss_weight(Dtype(1.));
    layer_param.mutable_loss_param()->set_normalization(
        LossParameter_NormalizationMode_NONE);
    SoftmaxParameter* softmax_param = layer_param.mutable_softmax_param();
    softmax_param->set_axis(1);
    // Fake reshape.
    vector<int> conf_shape(1, 1);
    conf_gt_.Reshape(conf_shape);
    conf_shape.push_back(num_classes_);
    conf_pred_.Reshape(conf_shape);
    conf_loss_layer_ = LayerRegistry<Dtype>::CreateLayer(layer_param);
    conf_loss_layer_->SetUp(conf_bottom_vec_, conf_top_vec_);
  }
  else if (conf_loss_type_ == MultiBoxLossParameter_ConfLossType_LOGISTIC) {
    LayerParameter layer_param;
    layer_param.set_name(this->layer_param_.name() + "_logistic_conf");
    layer_param.set_type("SigmoidCrossEntropyLoss");
    layer_param.add_loss_weight(Dtype(1.));
    // Fake reshape.
    vector<int> conf_shape(1, 1);
    conf_shape.push_back(num_classes_);
    conf_gt_.Reshape(conf_shape);
    conf_pred_.Reshape(conf_shape);
    conf_loss_layer_ = LayerRegistry<Dtype>::CreateLayer(layer_param);
    conf_loss_layer_->SetUp(conf_bottom_vec_, conf_top_vec_);
  } else {
    LOG(FATAL) << "Unknown confidence loss type.";
  }
}

template <typename Dtype>
void MultiBoxLossLayer<Dtype>::Reshape(const vector<Blob<Dtype>*>& bottom,
      const vector<Blob<Dtype>*>& top)
{
  LossLayer<Dtype>::Reshape(bottom, top);
  num_ = bottom[0]->num();// 图像的数量
  num_priors_ = bottom[2]->height() / 4; // priorbox的数量
  num_gt_ = bottom[3]->height();
  CHECK_EQ(bottom[0]->num(), bottom[1]->num());
  CHECK_EQ(num_priors_ * loc_classes_ * 4, bottom[0]->channels())
      << "Number of priors must match number of location predictions.";
  CHECK_EQ(num_priors_ * num_classes_, bottom[1]->channels())
      << "Number of priors must match number of confidence predictions.";
}

/*
 *
 * Forward_cpu的主要流程：
    FindMatches:确定哪些priorbox是正样本，哪些是负样本，存放在all_match_indices_中
    MineHardExamples：Minig出符合条件的负样本
    计算正样本的定位loss
    计算所有正样本+Mining出来的负样本的分类loss
    最后的loss为定位和分类loss的加权和
 *
 *
 */

template <typename Dtype>
void MultiBoxLossLayer<Dtype>::Forward_cpu(const vector<Blob<Dtype>*>& bottom,
    const vector<Blob<Dtype>*>& top)
{
  /*
   *
    bottom: "mbox_loc"
    bottom: "mbox_conf"
    bottom: "mbox_priorbox"
    bottom: "label"
    top: "mbox_loss"
   *
   */
  const Dtype* loc_data = bottom[0]->cpu_data(); // mbox_loc,用于定位
  const Dtype* conf_data = bottom[1]->cpu_data(); // mbox_conf，用于分类，表示置信度
  const Dtype* prior_data = bottom[2]->cpu_data();// mbox_priorbox，生成的所有box
  const Dtype* gt_data = bottom[3]->cpu_data(); // label，也就是batchsize图像的坐标

  // 获取batchsize中所有图像的label(目标在图像中的坐标)
  // Retrieve all ground truth.
  map<int, vector<NormalizedBBox> > all_gt_bboxes;
  GetGroundTruth(gt_data, num_gt_, background_label_id_, use_difficult_gt_,
                 &all_gt_bboxes);


  // 获取所有priorbbox的坐标和权重
  // Retrieve all prior bboxes. It is same within a batch since we assume all
  // images in a batch are of same dimension.
  // 一旦所有的priorbox参数设置好，对于每一幅图像来说，所有的default box都是一样的
  vector<NormalizedBBox> prior_bboxes;
  vector<vector<float> > prior_variances;
  GetPriorBBoxes(prior_data, num_priors_, &prior_bboxes, &prior_variances);

  // Retrieve all predictions.
  // 获取每幅图像的所有的位置预测,share_location为true时all_loc_preds中map<>中的first就是-1,all_loc_pred可以等价于vector<vector<NormalizedBBox>> all_loc_preds
  vector<LabelBBox> all_loc_preds; // typedef map<int, vector<NormalizedBBox> > LabelBBox;
  GetLocPredictions(loc_data,
                    num_, // 图像的数量
                    num_priors_, // priorbox的数量(这里num_priors是一幅图像的所有priorbox)
                    loc_classes_,// 1
                    share_location_, // true
                    &all_loc_preds);

  // Find matches between source bboxes and ground truth bboxes.
  /* 计算batchsize中每一幅图像中与每个priorbox的IOU最大( >overlap_threshold，比如0.5)的那个ground truth box的序号(如果没有序号为-1，overlap为0)
   * 这一步就是确定哪些是正样本，哪些是负样本,与mtcnn中生成正负样本的原理是一样的
   */
  vector<map<int, vector<float> > > all_match_overlaps;//
  FindMatches(all_loc_preds,// 所有的位置预测
              all_gt_bboxes,// batchsize中所有图像对应的label
              prior_bboxes,// 所有priorbbox的坐标和权重
              prior_variances,
              multibox_loss_param_,
              &all_match_overlaps,// batchsize中每一幅图像中与每个priorbox的IOU最大( >overlap_threshold，比如0.5)的groundtruth的IOU值,vector<map<int, vector<float> > > all_match_overlaps;，这里的map中first为label,由于share_location,所以first为-1
              &all_match_indices_);// batchsize中每一幅图像中与每个priorbox的IOU最大( >overlap_threshold，比如0.5)的那个ground truth box的序号，vector<map<int, vector<int> > > all_match_indices_;这里的map中first为label,由于share_location,所以first为-1

  num_matches_ = 0;// 所有图像中的正样本
  int num_negs = 0;

  // Sample hard negative (and positive) examples based on mining type.
  /* 做Mining,挑选出难例,由于要计算loss，所以需要知道priorbox的类别，所以先要FindMatches
   * 对每个priorbox进行分类和回归，计算分类loss,定位loss
       * MAX_NEGATIVE只针对负样本选择(如果只对负样本做Minig,则只计算分类loss，不计算定位loss)
       * HARD_EXAMPLE会同时对正和负样本做Mining(也就是会同时计算分类和定位loss)

    * 这里以MAX_NEGATIVE为例，挑选出符合条件的负样本
    *
    * MineHardExamples中ComputeLocLoss，ComputeConfLoss计算loss的时候，batchsize中每一幅图像独立计算
    * 因为最后Mine的时候，会对每一幅图像做Mining
   */
  MineHardExamples(*bottom[1], all_loc_preds, all_gt_bboxes, prior_bboxes,
                   prior_variances, all_match_overlaps, multibox_loss_param_,
                   &num_matches_, &num_negs, &all_match_indices_,
                   &all_neg_indices_);

  // 计算正样本的定位loss(batchsize幅图像中所有的正样本一起计算)
  if (num_matches_ >= 1)
  {
    // Form data to pass on to loc_loss_layer_.
    vector<int> loc_shape(2);
    loc_shape[0] = 1;
    loc_shape[1] = num_matches_ * 4; // 匹配到的数量*4
    loc_pred_.Reshape(loc_shape); // blob which stores the matched location prediction
    loc_gt_.Reshape(loc_shape); // blob which stores the corresponding matched ground truth
    Dtype* loc_pred_data = loc_pred_.mutable_cpu_data();
    Dtype* loc_gt_data = loc_gt_.mutable_cpu_data();


    // MineHardExamples中计算定位Loss的时候也是这么算的
    EncodeLocPrediction(all_loc_preds, // bottom[0]->cpu_data(); mbox_loc,用于定位
                        all_gt_bboxes, // batchsize中所有图像对应的坐标
                        all_match_indices_, // batchsize中每一幅图像的每个priorbox IOU最大的那个ground truth box的序号(如果没有就为-1)
                        prior_bboxes,// 所有priorbbox的坐标和权重
                        prior_variances,
                        multibox_loss_param_,
                        loc_pred_data,// batchsize幅图像中所有正样本priorbox的网络预测值(这里的正样本priorbox就是有匹配的priorbox)
                        loc_gt_data); // batchsize幅图像中所有正样本priorbox的groundtruth，即groundtruth与priorbox坐标的偏移量，也就是目标在priorbox中的坐标

    // 使用Smooth_L1 loss
    // Mining中计算loss的函数ComputeLocLoss也是使用的同样的原理，ComputeLocLoss中负样本的定位Loss为0
    // loc_bottom_vec_.push_back(&loc_pred_);
    // loc_bottom_vec_.push_back(&loc_gt_);
    // loc_top_vec_.push_back(&loc_loss_);
    loc_loss_layer_->Reshape(loc_bottom_vec_, loc_top_vec_);
    loc_loss_layer_->Forward(loc_bottom_vec_, loc_top_vec_);
  }
  else
  {
    loc_loss_.mutable_cpu_data()[0] = 0;
  }

  // 计算所有正样本+Mining出来的负样本的分类loss
  // Form data to pass on to conf_loss_layer_.
  if (do_neg_mining_)
  {
    num_conf_ = num_matches_ + num_negs; // 所有的正样本加上Mining出来的负样本
  }
  else
  {
    num_conf_ = num_ * num_priors_;
  }

  if (num_conf_ >= 1)
  {
    // Reshape the confidence data.
    vector<int> conf_shape;
    if (conf_loss_type_ == MultiBoxLossParameter_ConfLossType_SOFTMAX)
    {
      conf_shape.push_back(num_conf_);
      conf_gt_.Reshape(conf_shape);
      conf_shape.push_back(num_classes_);
      conf_pred_.Reshape(conf_shape);
    }
    else if (conf_loss_type_ == MultiBoxLossParameter_ConfLossType_LOGISTIC) {
      conf_shape.push_back(1);
      conf_shape.push_back(num_conf_);
      conf_shape.push_back(num_classes_);
      conf_gt_.Reshape(conf_shape);
      conf_pred_.Reshape(conf_shape);
    } else {
      LOG(FATAL) << "Unknown confidence loss type.";
    }
    if (!do_neg_mining_) {
      // Consider all scores.
      // Share data and diff with bottom[1].
      CHECK_EQ(conf_pred_.count(), bottom[1]->count());
      conf_pred_.ShareData(*(bottom[1]));
    }
    Dtype* conf_pred_data = conf_pred_.mutable_cpu_data();// blob which stores the confidence prediction.
    Dtype* conf_gt_data = conf_gt_.mutable_cpu_data();// blob which stores the corresponding ground truth label.
    caffe_set(conf_gt_.count(), Dtype(background_label_id_), conf_gt_data);


    // 计算分类loss，要知道网络预测值和groundtruth
    EncodeConfPrediction(conf_data, // mbox_conf，用于分类，表示置信度
                         num_,
                         num_priors_,
                         multibox_loss_param_,
                         all_match_indices_,// batchsize中每一幅图像的每个priorbox IOU最大的那个ground truth box的序号(如果没有就为-1)
                         all_neg_indices_, // 只计算hard样本
                         all_gt_bboxes,// batchsize中所有图像对应的坐标
                         conf_pred_data,// 所有正样本+Mining出来的负样本的priorbbox的网络预测值
                         conf_gt_data);// conf_pred_data中所有样本的label

    conf_loss_layer_->Reshape(conf_bottom_vec_, conf_top_vec_);// conf_bottom_vec_.push_back(&conf_pred_);conf_bottom_vec_.push_back(&conf_gt_);
    conf_loss_layer_->Forward(conf_bottom_vec_, conf_top_vec_);// conf_loss_.Reshape(loss_shape);
  }
  else
  {
    conf_loss_.mutable_cpu_data()[0] = 0;
  }

  // 最后的loss为定位和分类loss的加权和
  top[0]->mutable_cpu_data()[0] = 0;
  if (this->layer_param_.propagate_down(0))
  {
    Dtype normalizer = LossLayer<Dtype>::GetNormalizer(normalization_, num_, num_priors_, num_matches_);
    top[0]->mutable_cpu_data()[0] +=loc_weight_ * loc_loss_.cpu_data()[0] / normalizer;
  }

  if (this->layer_param_.propagate_down(1))
  {
    Dtype normalizer = LossLayer<Dtype>::GetNormalizer(normalization_, num_, num_priors_, num_matches_);
    top[0]->mutable_cpu_data()[0] += conf_loss_.cpu_data()[0] / normalizer;
  }
}

template <typename Dtype>
void MultiBoxLossLayer<Dtype>::Backward_cpu(const vector<Blob<Dtype>*>& top,
    const vector<bool>& propagate_down,
    const vector<Blob<Dtype>*>& bottom) {

  if (propagate_down[2]) {
    LOG(FATAL) << this->type()
        << " Layer cannot backpropagate to prior inputs.";
  }
  if (propagate_down[3]) {
    LOG(FATAL) << this->type()
        << " Layer cannot backpropagate to label inputs.";
  }

  // Back propagate on location prediction.
  if (propagate_down[0]) {
    Dtype* loc_bottom_diff = bottom[0]->mutable_cpu_diff();
    caffe_set(bottom[0]->count(), Dtype(0), loc_bottom_diff);
    if (num_matches_ >= 1) {
      vector<bool> loc_propagate_down;
      // Only back propagate on prediction, not ground truth.
      loc_propagate_down.push_back(true);
      loc_propagate_down.push_back(false);
      loc_loss_layer_->Backward(loc_top_vec_, loc_propagate_down,
                                loc_bottom_vec_);
      // Scale gradient.
      Dtype normalizer = LossLayer<Dtype>::GetNormalizer(
          normalization_, num_, num_priors_, num_matches_);
      Dtype loss_weight = top[0]->cpu_diff()[0] / normalizer;
      caffe_scal(loc_pred_.count(), loss_weight, loc_pred_.mutable_cpu_diff());
      // Copy gradient back to bottom[0].
      const Dtype* loc_pred_diff = loc_pred_.cpu_diff();
      int count = 0;
      for (int i = 0; i < num_; ++i) {
        for (map<int, vector<int> >::iterator it =
             all_match_indices_[i].begin();
             it != all_match_indices_[i].end(); ++it) {
          const int label = share_location_ ? 0 : it->first;
          const vector<int>& match_index = it->second;
          for (int j = 0; j < match_index.size(); ++j) {
            if (match_index[j] <= -1) {
              continue;
            }
            // Copy the diff to the right place.
            int start_idx = loc_classes_ * 4 * j + label * 4;
            caffe_copy<Dtype>(4, loc_pred_diff + count * 4,
                              loc_bottom_diff + start_idx);
            ++count;
          }
        }
        loc_bottom_diff += bottom[0]->offset(1);
      }
    }
  }

  // Back propagate on confidence prediction.
  if (propagate_down[1]) {
    Dtype* conf_bottom_diff = bottom[1]->mutable_cpu_diff();
    caffe_set(bottom[1]->count(), Dtype(0), conf_bottom_diff);
    if (num_conf_ >= 1) {
      vector<bool> conf_propagate_down;
      // Only back propagate on prediction, not ground truth.
      conf_propagate_down.push_back(true);
      conf_propagate_down.push_back(false);
      conf_loss_layer_->Backward(conf_top_vec_, conf_propagate_down,
                                 conf_bottom_vec_);
      // Scale gradient.
      Dtype normalizer = LossLayer<Dtype>::GetNormalizer(
          normalization_, num_, num_priors_, num_matches_);
      Dtype loss_weight = top[0]->cpu_diff()[0] / normalizer;
      caffe_scal(conf_pred_.count(), loss_weight,
                 conf_pred_.mutable_cpu_diff());
      // Copy gradient back to bottom[1].
      const Dtype* conf_pred_diff = conf_pred_.cpu_diff();
      if (do_neg_mining_) {
        int count = 0;
        for (int i = 0; i < num_; ++i) {
          // Copy matched (positive) bboxes scores' diff.
          const map<int, vector<int> >& match_indices = all_match_indices_[i];
          for (map<int, vector<int> >::const_iterator it =
               match_indices.begin(); it != match_indices.end(); ++it) {
            const vector<int>& match_index = it->second;
            CHECK_EQ(match_index.size(), num_priors_);
            for (int j = 0; j < num_priors_; ++j) {
              if (match_index[j] <= -1) {
                continue;
              }
              // Copy the diff to the right place.
              caffe_copy<Dtype>(num_classes_,
                                conf_pred_diff + count * num_classes_,
                                conf_bottom_diff + j * num_classes_);
              ++count;
            }
          }
          // Copy negative bboxes scores' diff.
          for (int n = 0; n < all_neg_indices_[i].size(); ++n) {
            int j = all_neg_indices_[i][n];
            CHECK_LT(j, num_priors_);
            caffe_copy<Dtype>(num_classes_,
                              conf_pred_diff + count * num_classes_,
                              conf_bottom_diff + j * num_classes_);
            ++count;
          }
          conf_bottom_diff += bottom[1]->offset(1);
        }
      } else {
        // The diff is already computed and stored.
        bottom[1]->ShareDiff(conf_pred_);
      }
    }
  }

  // After backward, remove match statistics.
  all_match_indices_.clear();
  all_neg_indices_.clear();
}

INSTANTIATE_CLASS(MultiBoxLossLayer);
REGISTER_LAYER_CLASS(MultiBoxLoss);

}  // namespace caffe
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
其中有几个比较重要的函数FindMatches(),MineHardExamples(),下面对他们详细解读一下

FindMatches
FindMatche函数就是寻找每一幅图像中与每个priorbox匹配的ground truth，这里匹配的意思就是所有IOU>阈值 中的最大的ground truth

void FindMatches(const vector<LabelBBox>& all_loc_preds,
      const map<int, vector<NormalizedBBox> >& all_gt_bboxes,
      const vector<NormalizedBBox>& prior_bboxes,
      const vector<vector<float> >& prior_variances,
      const MultiBoxLossParameter& multibox_loss_param,
      vector<map<int, vector<float> > >* all_match_overlaps,
      vector<map<int, vector<int> > >* all_match_indices)
{
  // all_match_overlaps->clear();
  // all_match_indices->clear();
  // Get parameters.
  CHECK(multibox_loss_param.has_num_classes()) << "Must provide num_classes.";
  const int num_classes = multibox_loss_param.num_classes();
  CHECK_GE(num_classes, 1) << "num_classes should not be less than 1.";
  const bool share_location = multibox_loss_param.share_location();//  true
  const int loc_classes = share_location ? 1 : num_classes; // 类别数
  const MatchType match_type = multibox_loss_param.match_type(); // match_type: PER_PREDICTION,per_prediction
  const float overlap_threshold = multibox_loss_param.overlap_threshold();// 0.5
  const bool use_prior_for_matching =multibox_loss_param.use_prior_for_matching(); // true
  const int background_label_id = multibox_loss_param.background_label_id();// 0
  const CodeType code_type = multibox_loss_param.code_type(); // CENTER_SIZE
  const bool encode_variance_in_target =multibox_loss_param.encode_variance_in_target(); // false
  const bool ignore_cross_boundary_bbox =multibox_loss_param.ignore_cross_boundary_bbox(); // false

  // Find the matches.
  int num = all_loc_preds.size();
  for (int i = 0; i < num; ++i) // 所有图像
  {
    map<int, vector<int> > match_indices;
    map<int, vector<float> > match_overlaps;
    // Check if there is ground truth for current image.
    if (all_gt_bboxes.find(i) == all_gt_bboxes.end())
    {
      // There is no gt for current image. All predictions are negative.
      all_match_indices->push_back(match_indices);
      all_match_overlaps->push_back(match_overlaps);
      continue;
    }
    // Find match between predictions and ground truth.
    const vector<NormalizedBBox>& gt_bboxes = all_gt_bboxes.find(i)->second;
    if (!use_prior_for_matching)
    {
      for (int c = 0; c < loc_classes; ++c)
      {
        int label = share_location ? -1 : c;
        if (!share_location && label == background_label_id)
        {
          // Ignore background loc predictions.
          continue;
        }
        // Decode the prediction into bbox first.
        vector<NormalizedBBox> loc_bboxes;
        bool clip_bbox = false;
        DecodeBBoxes(prior_bboxes, prior_variances,
                     code_type, encode_variance_in_target, clip_bbox,
                     all_loc_preds[i].find(label)->second, &loc_bboxes);
        MatchBBox(gt_bboxes, loc_bboxes, label, match_type,
                  overlap_threshold, ignore_cross_boundary_bbox,
                  &match_indices[label], &match_overlaps[label]);
      }
    }
    else
    {
      // Use prior bboxes to match against all ground truth.
      vector<int> temp_match_indices; // 存放batchsize中每一幅图像的每个priorbox IOU最大的那个ground truth box
      vector<float> temp_match_overlaps; // 存放batchsize中每一幅图像的每个priorbox IOU最大的那个ground truth box的IOU值
      const int label = -1;
      // 对每一幅图像的ground-truth bbox和prior_bboxes 进行匹配
      // 计算每个与priorbbox的IOU最大(>overlap_threshold)的那个ground truth
      MatchBBox(gt_bboxes, prior_bboxes, label, match_type, overlap_threshold,
                ignore_cross_boundary_bbox, &temp_match_indices,
                &temp_match_overlaps);
      if (share_location)
      {
        match_indices[label] = temp_match_indices;
        match_overlaps[label] = temp_match_overlaps;
      }
      else
      {
        // Get ground truth label for each ground truth bbox.
        vector<int> gt_labels;
        for (int g = 0; g < gt_bboxes.size(); ++g)
        {
          gt_labels.push_back(gt_bboxes[g].label());
        }
        // Distribute the matching results to different loc_class.
        for (int c = 0; c < loc_classes; ++c)
        {
          if (c == background_label_id)
          {
            // Ignore background loc predictions.
            continue;
          }
          match_indices[c].resize(temp_match_indices.size(), -1);
          match_overlaps[c] = temp_match_overlaps;
          for (int m = 0; m < temp_match_indices.size(); ++m)
          {
            if (temp_match_indices[m] > -1)
            {
              const int gt_idx = temp_match_indices[m];
              CHECK_LT(gt_idx, gt_labels.size());
              if (c == gt_labels[gt_idx])
              {
                match_indices[c][m] = gt_idx;
              }
            }
          }
        }
      }
    }
    all_match_indices->push_back(match_indices);
    all_match_overlaps->push_back(match_overlaps);
  }
}

void MatchBBox(const vector<NormalizedBBox>& gt_bboxes,
    const vector<NormalizedBBox>& pred_bboxes, const int label,// const int label = -1;
    const MatchType match_type, const float overlap_threshold,
    const bool ignore_cross_boundary_bbox, // false
    vector<int>* match_indices, vector<float>* match_overlaps)
{
  int num_pred = pred_bboxes.size();
  match_indices->clear();
  match_indices->resize(num_pred, -1);
  match_overlaps->clear();
  match_overlaps->resize(num_pred, 0.);

  int num_gt = 0;
  vector<int> gt_indices;
  if (label == -1)
  {
    // label -1 means comparing against all ground truth.
    num_gt = gt_bboxes.size();
    for (int i = 0; i < num_gt; ++i)
    {
      gt_indices.push_back(i);
    }
  }
  else
  {
    // Count number of ground truth boxes which has the desired label.
    for (int i = 0; i < gt_bboxes.size(); ++i)
    {
      if (gt_bboxes[i].label() == label)
      {
        num_gt++;
        gt_indices.push_back(i);
      }
    }
  }
  if (num_gt == 0)
  {
    return;
  }

  // Store the positive overlap between predictions and ground truth.
  map<int, map<int, float> > overlaps; // 该priorbox与每个ground truth box的IOU

  // 计算与每个priorbbox有交集的最大IOU的ground truth box
  for (int i = 0; i < num_pred; ++i)
  {
    if (ignore_cross_boundary_bbox && IsCrossBoundaryBBox(pred_bboxes[i]))
    {
      (*match_indices)[i] = -2;
      continue;
    }
    for (int j = 0; j < num_gt; ++j)
    {
      float overlap = JaccardOverlap(pred_bboxes[i], gt_bboxes[gt_indices[j]]);

      // 有交集
      if (overlap > 1e-6)
      {
         // 计算最大的IOU
         // 计算与第i个priorbbox的IOU最大的ground truth
        (*match_overlaps)[i] = std::max((*match_overlaps)[i], overlap);
        overlaps[i][j] = overlap; // 保存所有的IOU的值
      }
    }
  }

  // Bipartite matching.
  vector<int> gt_pool;
  for (int i = 0; i < num_gt; ++i)
  {
    gt_pool.push_back(i);
  }
  while (gt_pool.size() > 0)
  {
    // Find the most overlapped gt and cooresponding predictions.
    int max_idx = -1;
    int max_gt_idx = -1;
    float max_overlap = -1;
    for (map<int, map<int, float> >::iterator it = overlaps.begin();it != overlaps.end(); ++it)
    {
      int i = it->first;// priorbox的序号
      if ((*match_indices)[i] != -1)
      {
        // The prediction already has matched ground truth or is ignored.
        continue;
      }

      // 遍历该prior box与所有ground truth box的IOU,找出最大的IOU对应的ground truth
      for (int p = 0; p < gt_pool.size(); ++p)
      {
        int j = gt_pool[p]; // ground truth的序号
        if (it->second.find(j) == it->second.end())
        {
          // No overlap between the i-th prediction and j-th ground truth.
          continue;
        }
        // Find the maximum overlapped pair.
        if (it->second[j] > max_overlap)
        {
          // If the prediction has not been matched to any ground truth,
          // and the overlap is larger than maximum overlap, update.
          max_idx = i;
          max_gt_idx = j;
          max_overlap = it->second[j];
        }
      }
    }
    if (max_idx == -1)
    {
      // Cannot find good match.
      break;
    }
    else
    {
      CHECK_EQ((*match_indices)[max_idx], -1);

      (*match_indices)[max_idx] = gt_indices[max_gt_idx];
      (*match_overlaps)[max_idx] = max_overlap;

      // Erase the ground truth.
      gt_pool.erase(std::find(gt_pool.begin(), gt_pool.end(), max_gt_idx));
    }
  }

  switch (match_type)
  {
    case MultiBoxLossParameter_MatchType_BIPARTITE:
      // Already done.
      break;
    case MultiBoxLossParameter_MatchType_PER_PREDICTION:
      // Get most overlaped for the rest prediction bboxes.
      for (map<int, map<int, float> >::iterator it = overlaps.begin();
           it != overlaps.end(); ++it)
      {
        int i = it->first;
        if ((*match_indices)[i] != -1)
        {
          // The prediction already has matched ground truth or is ignored.
          continue;
        }
        int max_gt_idx = -1;
        float max_overlap = -1;
        for (int j = 0; j < num_gt; ++j)
        {
          if (it->second.find(j) == it->second.end())
          {
            // No overlap between the i-th prediction and j-th ground truth.
            continue;
          }
          // Find the maximum overlapped pair.
          float overlap = it->second[j];
          if (overlap >= overlap_threshold && overlap > max_overlap)
          {
            // If the prediction has not been matched to any ground truth,
            // and the overlap is larger than maximum overlap, update.
            max_gt_idx = j;
            max_overlap = overlap;
          }
        }
        if (max_gt_idx != -1)
        {
          // Found a matched ground truth.
          CHECK_EQ((*match_indices)[i], -1);

          // 寻找到了最大的ground truth,以及最大的IOU
          (*match_indices)[i] = gt_indices[max_gt_idx]; // 与第i个priorbox的IOU最大的是第gt_indices[max_gt_idx]即max_gt_idx个ground truth
          (*match_overlaps)[i] = max_overlap;
        }
      }
      break;
    default:
      LOG(FATAL) << "Unknown matching type.";
      break;
  }

  return;
}

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
MineHardExamples
MineHardExamples就是做Mining的

template <typename Dtype>
void MineHardExamples(const Blob<Dtype>& conf_blob,
    const vector<LabelBBox>& all_loc_preds,
    const map<int, vector<NormalizedBBox> >& all_gt_bboxes,
    const vector<NormalizedBBox>& prior_bboxes,
    const vector<vector<float> >& prior_variances,
    const vector<map<int, vector<float> > >& all_match_overlaps,
    const MultiBoxLossParameter& multibox_loss_param,
    int* num_matches, int* num_negs,
    vector<map<int, vector<int> > >* all_match_indices,
    vector<vector<int> >* all_neg_indices)
{
  int num = all_loc_preds.size();
  // CHECK_EQ(num, all_match_overlaps.size());
  // CHECK_EQ(num, all_match_indices->size());
  // all_neg_indices->clear();
  *num_matches = CountNumMatches(*all_match_indices, num);// 所有图像中的正样本
  *num_negs = 0;
  int num_priors = prior_bboxes.size();
  CHECK_EQ(num_priors, prior_variances.size());
  // Get parameters.
  CHECK(multibox_loss_param.has_num_classes()) << "Must provide num_classes.";
  const int num_classes = multibox_loss_param.num_classes();
  CHECK_GE(num_classes, 1) << "num_classes should not be less than 1.";
  const int background_label_id = multibox_loss_param.background_label_id();
  const bool use_prior_for_nms = multibox_loss_param.use_prior_for_nms();
  const ConfLossType conf_loss_type = multibox_loss_param.conf_loss_type();
  const MiningType mining_type = multibox_loss_param.mining_type();
  if (mining_type == MultiBoxLossParameter_MiningType_NONE)
  {
    return;
  }
  const LocLossType loc_loss_type = multibox_loss_param.loc_loss_type();
  const float neg_pos_ratio = multibox_loss_param.neg_pos_ratio();
  const float neg_overlap = multibox_loss_param.neg_overlap();
  const CodeType code_type = multibox_loss_param.code_type();
  const bool encode_variance_in_target =
      multibox_loss_param.encode_variance_in_target();
  const bool has_nms_param = multibox_loss_param.has_nms_param();
  float nms_threshold = 0;
  int top_k = -1;
  if (has_nms_param)
  {
    nms_threshold = multibox_loss_param.nms_param().nms_threshold();
    top_k = multibox_loss_param.nms_param().top_k();
  }
  const int sample_size = multibox_loss_param.sample_size();
  // Compute confidence losses based on matching results.
  vector<vector<float> > all_conf_loss;
#ifdef CPU_ONLY

  /*计算batchsize中每一幅图像每个priorbox的分类loss(softmax loss)，每个priorbox的类别是通过是否有对应的groundtruth来决定的(有就是正样本，没有就是负)
   *
    总结：
    MineHardExamples中ComputeConfLoss，EncodeLocPrediction，ComputeLocLoss基本采用的是相同的思路：

    // 遍历batchsize中的每一幅图像
    for (int i = 0; i < num; ++i)
    {
        // 获取每幅图像中与每个priorbox匹配的那个ground truth的序号(其实就是与每个priorbox的IOU最大的那个ground-truth的序号)
        const vector<int>& match_index;

        // 遍历每一个priorbox
        for (int j = 0; j < match_index.size(); ++j)
        {
            // 负样本
            if (match_index[j] <= -1)
            {
            }
        }

    }

   */
  ComputeConfLoss(conf_blob.cpu_data(),
                  num,
                  num_priors,
                  num_classes,// 21,分类类别数
                  background_label_id,
                  conf_loss_type,
                  *all_match_indices,
                  all_gt_bboxes,
                  &all_conf_loss);
#else
  ComputeConfLossGPU(conf_blob, num, num_priors, num_classes,
      background_label_id, conf_loss_type, *all_match_indices, all_gt_bboxes,
      &all_conf_loss);
#endif
  /* 计算batchsize中每一幅图像的每个priorbox的定位loss(负样本为0)
       * MAX_NEGATIVE只针对负样本选择(如果只对负样本做Minig,则只计算分类loss，不计算定位loss)
       * HARD_EXAMPLE会同时对正和负样本做Mining(也就是会同时计算分类和定位loss)
   */
  vector<vector<float> > all_loc_loss;// 如果是MAX_NEGATIVE，设置为0
  if (mining_type == MultiBoxLossParameter_MiningType_HARD_EXAMPLE)
  {
    // Compute localization losses based on matching results.
    Blob<Dtype> loc_pred, loc_gt;
    if (*num_matches != 0)
    {
      vector<int> loc_shape(2, 1);
      loc_shape[1] = *num_matches * 4;
      loc_pred.Reshape(loc_shape);
      loc_gt.Reshape(loc_shape);
      Dtype* loc_pred_data = loc_pred.mutable_cpu_data();
      Dtype* loc_gt_data = loc_gt.mutable_cpu_data();

      // 计算batchsize幅图像所有正样本的预测值和ground truth
      EncodeLocPrediction(all_loc_preds,
                          all_gt_bboxes,
                          *all_match_indices,
                          prior_bboxes,
                          prior_variances,
                          multibox_loss_param,
                          loc_pred_data, // batchsize幅图像中所有正样本priorbox的网络预测值(这里的正样本priorbox就是有匹配的priorbox)
                          loc_gt_data); // batchsize幅图像中所有正样本priorbox的groundtruth，即groundtruth与priorbox坐标的偏移量，也就是目标在priorbox中的坐标
    }

    // 计算batchsize中每一幅图像的每个priorbox的定位loss,这个loss就是|网络预测值-正样本priorbox与ground truth的偏移|
    // 对于负样本，该loss为0
    ComputeLocLoss(loc_pred, loc_gt, *all_match_indices, num,
                   num_priors, loc_loss_type, &all_loc_loss);
  }
  else
  {
    // No localization loss.
    for (int i = 0; i < num; ++i) {
      vector<float> loc_loss(num_priors, 0.f);
      all_loc_loss.push_back(loc_loss);
    }
  }

  // 每一幅图像独立计算
  for (int i = 0; i < num; ++i)
  {
    map<int, vector<int> >& match_indices = (*all_match_indices)[i];
    const map<int, vector<float> >& match_overlaps = all_match_overlaps[i];

    // loc + conf loss.
    const vector<float>& conf_loss = all_conf_loss[i];
    const vector<float>& loc_loss = all_loc_loss[i];
    vector<float> loss;
    std::transform(conf_loss.begin(), conf_loss.end(), loc_loss.begin(),
                   std::back_inserter(loss), std::plus<float>());

    // Pick negatives or hard examples based on loss.
    // 基于定位和分类两个loss做mining，这里以MAX_NEGATIVE为例
    set<int> sel_indices;
    vector<int> neg_indices; // 每幅图像选择出来的负样本priorbox的序号
    for (map<int, vector<int> >::iterator it = match_indices.begin();it != match_indices.end(); ++it)
    {
      const int label = it->first;
      int num_sel = 0;
      // Get potential indices and loss pairs.
      // 挑选所有负样本prior_box的loss和该priorbox的序号
      /*这里假设为MAX_NEGATIVE
       * MAX_NEGATIVE只针对负样本选择(如果只对负样本做Minig,则只计算分类loss，不计算定位loss)
       * HARD_EXAMPLE会同时对正和负样本做Mining(也就是会同时计算分类和定位loss)
        // Mining type during training.
        //   NONE : use all negatives.
        //   MAX_NEGATIVE : select negatives based on the score.
        //   HARD_EXAMPLE : select hard examples based on "Training Region-based Object Detectors with Online Hard Example Mining", Shrivastava et.al.
       */
      vector<pair<float, int> > loss_indices;
      for (int m = 0; m < match_indices[label].size(); ++m) // 遍历每一个priorbox
      {
        // 对于MAX_NEGATIVE，判断是否为负样本
        if (IsEligibleMining(mining_type, match_indices[label][m],match_overlaps.find(label)->second[m], neg_overlap)) 
        {
          // 该prior_box的loss和该priorbox的序号
          loss_indices.push_back(std::make_pair(loss[m], m));
          ++num_sel;
        }
      }
      if (mining_type == MultiBoxLossParameter_MiningType_MAX_NEGATIVE)
        {
          // 计算正样本个数
        int num_pos = 0;
        for (int m = 0; m < match_indices[label].size(); ++m) // 判断每个Priorbox的类别
        {
          if (match_indices[label][m] > -1)
          {
            ++num_pos;
          }
        }
        // 计算负样本的个数
        num_sel = std::min(static_cast<int>(num_pos * neg_pos_ratio), num_sel);
      } else if (mining_type == MultiBoxLossParameter_MiningType_HARD_EXAMPLE) {
        CHECK_GT(sample_size, 0);
        num_sel = std::min(sample_size, num_sel);
      }
      // Select samples，这里执行else
      if (has_nms_param && nms_threshold > 0)
      {
        // Do nms before selecting samples.
        vector<float> sel_loss;
        vector<NormalizedBBox> sel_bboxes;
        if (use_prior_for_nms) {
          for (int m = 0; m < match_indices[label].size(); ++m)
          {
            if (IsEligibleMining(mining_type, match_indices[label][m],
                match_overlaps.find(label)->second[m], neg_overlap))
            {
              sel_loss.push_back(loss[m]);
              sel_bboxes.push_back(prior_bboxes[m]);
            }
          }
        }
        else
        {
          // Decode the prediction into bbox first.
          vector<NormalizedBBox> loc_bboxes;
          bool clip_bbox = false;
          DecodeBBoxes(prior_bboxes, prior_variances,
                       code_type, encode_variance_in_target, clip_bbox,
                       all_loc_preds[i].find(label)->second, &loc_bboxes);
          for (int m = 0; m < match_indices[label].size(); ++m)
          {
            if (IsEligibleMining(mining_type, match_indices[label][m],match_overlaps.find(label)->second[m], neg_overlap)) 
            {
              sel_loss.push_back(loss[m]);
              sel_bboxes.push_back(loc_bboxes[m]);
            }
          }
        }
        // Do non-maximum suppression based on the loss.
        vector<int> nms_indices;
        ApplyNMS(sel_bboxes, sel_loss, nms_threshold, top_k, &nms_indices);
        if (nms_indices.size() < num_sel) {
          LOG(INFO) << "not enough sample after nms: " << nms_indices.size();
        }
        // Pick top example indices after nms.
        num_sel = std::min(static_cast<int>(nms_indices.size()), num_sel);
        for (int n = 0; n < num_sel; ++n) {
          sel_indices.insert(loss_indices[nms_indices[n]].second);
        }
      }
      else
      {
         // 对负样本的loss排序
        // Pick top example indices based on loss.
        std::sort(loss_indices.begin(), loss_indices.end(),SortScorePairDescend<int>);

        // 选择符合条件的负样本
        for (int n = 0; n < num_sel; ++n)
        {
          sel_indices.insert(loss_indices[n].second);
        }
      }
      // Update the match_indices and select neg_indices.
      for (int m = 0; m < match_indices[label].size(); ++m)
      {
        if (match_indices[label][m] > -1)
        {
          if (mining_type == MultiBoxLossParameter_MiningType_HARD_EXAMPLE &&sel_indices.find(m) == sel_indices.end())
          {
            match_indices[label][m] = -1;
            *num_matches -= 1;
          }
        } else if (match_indices[label][m] == -1) {
          if (sel_indices.find(m) != sel_indices.end()) {
            neg_indices.push_back(m);// 负样本的priorbox
            *num_negs += 1;
          }
        }
      }
    }
    all_neg_indices->push_back(neg_indices); // 所有的hard sample
  }
}

// 计算所有priorbox的softmax loss，每个priorbox的类别是通过是否有对应的groundtruth来决定的
template <typename Dtype>
void ComputeConfLoss(const Dtype* conf_data, const int num,
      const int num_preds_per_class, // priorbox的数量
                     const int num_classes,// 21分类
      const int background_label_id, const ConfLossType loss_type,
      const vector<map<int, vector<int> > >& all_match_indices,
      const map<int, vector<NormalizedBBox> >& all_gt_bboxes,
      vector<vector<float> >* all_conf_loss)
{
  CHECK_LT(background_label_id, num_classes);

  // CHECK_EQ(num, all_match_indices.size());
  all_conf_loss->clear();
  for (int i = 0; i < num; ++i) // 每幅图像
  {
    vector<float> conf_loss;
    const map<int, vector<int> >& match_indices = all_match_indices[i];
    for (int p = 0; p < num_preds_per_class; ++p) // 每一幅图像所有priorbox
    {
      int start_idx = p * num_classes; // 该priorbox在预测中的起始位置

      // 获取该priorbox的label，priorbox的label通过是否有匹配的ground truth来确定
      int label = background_label_id;
      for (map<int, vector<int> >::const_iterator it =match_indices.begin(); it != match_indices.end(); ++it) 
      {
          // 每幅图像中与每个priorbox匹配的那个ground truth的序号(其实就是与每个priorbox的IOU最大的那个ground-truth的序号)
        const vector<int>& match_index = it->second;
        CHECK_EQ(match_index.size(), num_preds_per_class);
        if (match_index[p] > -1)  // 找到了该priorbox对应的groundtruth
        {
          CHECK(all_gt_bboxes.find(i) != all_gt_bboxes.end());
          const vector<NormalizedBBox>& gt_bboxes =
              all_gt_bboxes.find(i)->second;
          CHECK_LT(match_index[p], gt_bboxes.size());
          label = gt_bboxes[match_index[p]].label(); // 获取该priorbox的类别
          CHECK_GE(label, 0);
          CHECK_NE(label, background_label_id);
          CHECK_LT(label, num_classes);
          // A prior can only be matched to one gt bbox.
          break;
        }
      }

      // 计算softmax loss
      Dtype loss = 0;
      if (loss_type == MultiBoxLossParameter_ConfLossType_SOFTMAX)
      {
        CHECK_GE(label, 0);
        CHECK_LT(label, num_classes);
        // Compute softmax probability.
        // We need to subtract the max to avoid numerical issues.
        Dtype maxval = conf_data[start_idx];
        for (int c = 1; c < num_classes; ++c)
        {
          maxval = std::max<Dtype>(conf_data[start_idx + c], maxval);
        }
        Dtype sum = 0.;
        for (int c = 0; c < num_classes; ++c)
        {
          sum += std::exp(conf_data[start_idx + c] - maxval);
        }
        Dtype prob = std::exp(conf_data[start_idx + label] - maxval) / sum;
        loss = -log(std::max(prob, Dtype(FLT_MIN)));
      } else if (loss_type == MultiBoxLossParameter_ConfLossType_LOGISTIC) {
        int target = 0;
        for (int c = 0; c < num_classes; ++c) {
          if (c == label) {
            target = 1;
          } else {
            target = 0;
          }
          Dtype input = conf_data[start_idx + c];
          loss -= input * (target - (input >= 0)) -
              log(1 + exp(input - 2 * input * (input >= 0)));
        }
      } else {
        LOG(FATAL) << "Unknown conf loss type.";
      }
      conf_loss.push_back(loss);
    }
    conf_data += num_preds_per_class * num_classes;
    all_conf_loss->push_back(conf_loss);
  }
}

template <typename Dtype>
void EncodeLocPrediction(const vector<LabelBBox>& all_loc_preds, // LabelBBox中的first为-1
      const map<int, vector<NormalizedBBox> >& all_gt_bboxes,
      const vector<map<int, vector<int> > >& all_match_indices,
      const vector<NormalizedBBox>& prior_bboxes,
      const vector<vector<float> >& prior_variances,
      const MultiBoxLossParameter& multibox_loss_param,
      Dtype* loc_pred_data, // batchsize幅图像中所有正样本priorbox的网络预测值
        Dtype* loc_gt_data) // batchsize幅图像中所有正样本priorbox的groundtruth，即groundtruth与priorbox坐标的偏移量，也就是目标在priorbox中的坐标
{
  int num = all_loc_preds.size(); // 图片的数量
  // CHECK_EQ(num, all_match_indices.size());
  // Get parameters.
  const CodeType code_type = multibox_loss_param.code_type(); // CENTER_SIZE
  const bool encode_variance_in_target =multibox_loss_param.encode_variance_in_target(); // false
  const bool bp_inside = multibox_loss_param.bp_inside(); // false
  const bool use_prior_for_matching = multibox_loss_param.use_prior_for_matching();// true
  int count = 0; // 有匹配的priorbox的数量，也就是正样本的数量

  // 遍历batchsize中的每一幅图像
  for (int i = 0; i < num; ++i)
  {
    for (map<int, vector<int> >::const_iterator it = all_match_indices[i].begin();it != all_match_indices[i].end(); ++it)
    {
      const int label = it->first;
      const vector<int>& match_index = it->second; // 每幅图像中与每个priorbox匹配的那个ground truth的序号(其实就是与每个priorbox的IOU最大的那个ground-truth的序号)
      CHECK(all_loc_preds[i].find(label) != all_loc_preds[i].end());

      // 该幅图像中所有priorbox的预测坐标
      const vector<NormalizedBBox>& loc_pred =all_loc_preds[i].find(label)->second;

      // 通过match_index遍历每一个priorbox,判断是否是正样本，是的话计算偏移量，并保存该priorbox的预测值
      for (int j = 0; j < match_index.size(); ++j)
      {
        if (match_index[j] <= -1)
        {
          continue;
        }
        // Store encoded ground truth.
        const int gt_idx = match_index[j]; // 该幅图像中第j个priorbox对应的IOU最大的那个groundtruth
        CHECK(all_gt_bboxes.find(i) != all_gt_bboxes.end());
        CHECK_LT(gt_idx, all_gt_bboxes.find(i)->second.size());
        const NormalizedBBox& gt_bbox = all_gt_bboxes.find(i)->second[gt_idx]; // 该幅图像中第gt_idx的ground-truth box
        NormalizedBBox gt_encode;
        CHECK_LT(j, prior_bboxes.size());
        EncodeBBox(prior_bboxes[j],  //
                   prior_variances[j],
                   code_type, // center_size
                   encode_variance_in_target,// false
                   gt_bbox, // 与prior_bboxes[j] IOU最大的那个gt_bbox
                   &gt_encode); // gt_encode就是ground truth与对应的prior_bboxes的偏移量(这个ground truth就是与prior_bboxes的IOU最大的那个)
                                // (由于感受野的不同，感受的区域并不是priorbbox表示的区域，所以要重新计算坐标)
        loc_gt_data[count * 4] = gt_encode.xmin();
        loc_gt_data[count * 4 + 1] = gt_encode.ymin();
        loc_gt_data[count * 4 + 2] = gt_encode.xmax();
        loc_gt_data[count * 4 + 3] = gt_encode.ymax();
        // Store location prediction.
        CHECK_LT(j, loc_pred.size());
        if (bp_inside)
        {
          NormalizedBBox match_bbox = prior_bboxes[j];
          if (!use_prior_for_matching)
          {
            const bool clip_bbox = false;
            DecodeBBox(prior_bboxes[j], prior_variances[j], code_type,
                       encode_variance_in_target, clip_bbox, loc_pred[j],
                       &match_bbox);
          }
          // When a dimension of match_bbox is outside of image region, use
          // gt_encode to simulate zero gradient.
          loc_pred_data[count * 4] =
              (match_bbox.xmin() < 0 || match_bbox.xmin() > 1) ?
              gt_encode.xmin() : loc_pred[j].xmin();
          loc_pred_data[count * 4 + 1] =
              (match_bbox.ymin() < 0 || match_bbox.ymin() > 1) ?
              gt_encode.ymin() : loc_pred[j].ymin();
          loc_pred_data[count * 4 + 2] =
              (match_bbox.xmax() < 0 || match_bbox.xmax() > 1) ?
              gt_encode.xmax() : loc_pred[j].xmax();
          loc_pred_data[count * 4 + 3] =
              (match_bbox.ymax() < 0 || match_bbox.ymax() > 1) ?
              gt_encode.ymax() : loc_pred[j].ymax();
        }
        else
        {
          // 第j个prior bbox的预测值
          loc_pred_data[count * 4] = loc_pred[j].xmin();
          loc_pred_data[count * 4 + 1] = loc_pred[j].ymin();
          loc_pred_data[count * 4 + 2] = loc_pred[j].xmax();
          loc_pred_data[count * 4 + 3] = loc_pred[j].ymax();
        }
        if (encode_variance_in_target)
        {
          for (int k = 0; k < 4; ++k)
          {
            CHECK_GT(prior_variances[j][k], 0);
            loc_pred_data[count * 4 + k] /= prior_variances[j][k];
            loc_gt_data[count * 4 + k] /= prior_variances[j][k];
          }
        }
        ++count;
      }
    }
  }
}


template <typename Dtype>
void ComputeLocLoss(const Blob<Dtype>& loc_pred, const Blob<Dtype>& loc_gt,
      const vector<map<int, vector<int> > >& all_match_indices,
      const int num, const int num_priors, const LocLossType loc_loss_type,
      vector<vector<float> >* all_loc_loss)
{
  int loc_count = loc_pred.count();
  CHECK_EQ(loc_count, loc_gt.count());
  Blob<Dtype> diff;
  const Dtype* diff_data = NULL;
  if (loc_count != 0)
  {
    diff.Reshape(loc_pred.shape());
    caffe_sub(loc_count, loc_pred.cpu_data(), loc_gt.cpu_data(),
              diff.mutable_cpu_data());
    diff_data = diff.cpu_data();
  }
  int count = 0;
  for (int i = 0; i < num; ++i)
  {
    // 计算batchsizse中每幅图像每一个priorbox的定位loss
    vector<float> loc_loss(num_priors, 0.f); // 初始化都为0
    for (map<int, vector<int> >::const_iterator it = all_match_indices[i].begin();it != all_match_indices[i].end(); ++it)
    {
        // 每幅图像中与每个priorbox匹配的那个ground truth的序号(其实就是与每个priorbox的IOU最大的那个ground-truth的序号)
      const vector<int>& match_index = it->second;
      CHECK_EQ(num_priors, match_index.size());

      // 遍历所有的priorbox，计算正样本的定位loss
      // 这个loss其实就是计算了 |ground truth与priorbox之间偏移量- 该priorbox对应的预测值|
      for (int j = 0; j < match_index.size(); ++j)
      {
        if (match_index[j] <= -1)
        {
          continue;
        }

        // 只针对matched priorbox计算loss
        Dtype loss = 0;
        for (int k = 0; k < 4; ++k)
        {
          Dtype val = diff_data[count * 4 + k];
          if (loc_loss_type == MultiBoxLossParameter_LocLossType_SMOOTH_L1)
          {
            Dtype abs_val = fabs(val); // 计算L1距离
            if (abs_val < 1.)
            {
              loss += 0.5 * val * val;
            }
            else
            {
              loss += abs_val - 0.5;
            }
          } else if (loc_loss_type == MultiBoxLossParameter_LocLossType_L2)
          {
            loss += 0.5 * val * val;
          } else {
            LOG(FATAL) << "Unknown loc loss type.";
          }
        }
        loc_loss[j] = loss;
        ++count;
      }
    }
    all_loc_loss->push_back(loc_loss);
  }
}