# 扩充评测集

先装开发依赖：`pip install -e ".[ocr,dev]"`。

1. 在 `eval/labels.yaml`（或新建一个 yaml）里加条目：
   - `label`：可以是列表，表示可接受的多个标签
   - `segments`：分段真值
   - `real_material`：是否用了真实素材
   - `cuts` / `cut_tolerance`：切点真值
   - `audio`：`{voice, music, sfx, bpm, key}`
2. 真值要有出处，写在 `source` 字段：生产记录（timeline.json、manifest、cues.py）> 平台 AIGC 标识 > 人工目测（目测的要写"存疑"）。
3. 跑 `rea-video eval eval/xxx.yaml -o out/eval_xxx`。只改分类规则时不用重新解码：评测会用缓存特征重新分类；改了测量视频的代码（解码、切镜、特征、声音、包装）会自动重新解码，不会拿旧特征给新代码打分（`--fresh` 全部重来，`--only id` 只重解指定视频）。清单里的路径找不到时会用 `eval/media/<id>.<扩展名>` 里的备份，仍然缺的会在摘要的 `missing` 里列出。
4. 调规则要防止过拟合：至少保留一组**改规则之后才第一次跑**的留出集，结果写进 `eval/RESULTS.md`。
