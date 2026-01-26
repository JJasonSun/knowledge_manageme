



## 2. 题型定义表 (exercise_types)

定义具体的交互形式（如“听音选图”、“朗读句子”）。

| **字段名**  | **类型** | **说明** | **科学性/逻辑备注**                                                   |
| ----------------- | -------------- | -------------- | --------------------------------------------------------------------------- |
| id                | UUID           | 主键           |                                                                             |
| skill_category_id | UUID           | **外键** | 关联 `skill_categories`。这建立了从“具体题目”到“宏观技能”的映射路径。 |
| name              | VARCHAR(255)   | 组件标识       | 唯一键。前端根据此字段决定渲染哪个 Vue/React 组件。                         |
| display_name      | VARCHAR(255)   | 展示名称       |                                                                             |
| description       | TEXT           | 描述           |                                                                             |
| display_order     | INT4           | 排序           | 组内唯一。                                                                  |

id | skill_category_id | name | display_name| description| display_order
71282795-c6ee-48ef-a3fe-cc087b13fbaa	d0e546d8-4b98-4edc-bc52-106d94ff421b	LISTEN_IMAGE_TRUE_FALSE	听录音，看图判断		1
0b94285e-8b08-4135-949b-95c7d90a1cc4	d0e546d8-4b98-4edc-bc52-106d94ff421b	LISTEN_IMAGE_MC	听录音，看图选择		2
81b917f5-5dbc-4b20-aabe-57871c0babaa	d0e546d8-4b98-4edc-bc52-106d94ff421b	LISTEN_IMAGE_MATCH	听录音，看图配对		3
22b4f70e-5764-444a-9340-1f8621516676	d0e546d8-4b98-4edc-bc52-106d94ff421b	LISTEN_SENTENCE_QA	听录音，句子问答		4
f4ad51e5-6290-408a-a072-d35c5c73627f	d0e546d8-4b98-4edc-bc52-106d94ff421b	LISTEN_SENTENCE_TF	听录音，句子判断		5
e0e22f43-a812-4b0e-a88d-e4d786ca5d0b	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_IMAGE_TRUE_FALSE	阅读，图片判断		6
3b1add22-9af4-4e69-99eb-26ef785d4f3b	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_IMAGE_MATCH	阅读，看图配对		7
a9a8ea45-f888-43f5-95f6-46b5e07247db	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_DIALOGUE_MATCH	阅读，对话配对		8
f638e0d2-ac87-4605-a1f4-c2499311018a	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_WORD_GAP_FILL	阅读，句子填空		9
147ebae1-9f54-46e2-925d-65adda4692d8	8ca0dedb-466e-41aa-aa2f-2310853f499a	READ_SENTENCE_TRANSLATION	句子翻译		10
a1ea7fa4-efe4-4048-a78c-e6b9bc162fe4	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_SENTENCE_TF	句子理解(判断)		12
41abcea3-2f25-4a53-a083-fb1f7ef82aac	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_SENTENCE_COMPREHENSION_CHOICE	句子理解(选择)		11
2c4d174c-6a7c-47b0-b9c7-9d454fcdc927	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_PARAGRAPH_COMPREHENSION	段落理解		13
dbe329a7-8ba1-40ae-b379-4cefef45613e	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_WORD_ORDER	连词成句		14
0b0fb57b-9ba8-4f4d-803a-3832a2beac69	d0e546d8-4b98-4edc-bc52-106d94ff421b	LISTEN_DIALOGUE_QA	听力，对话问答		15
7f750f17-c132-4078-8130-ae9f8bd3ab00	d0e546d8-4b98-4edc-bc52-106d94ff421b	LISTEN_PARAGRAPH_QA	听力，段落问答		16
8cbf4d79-3070-44a4-b72f-d1d21f794766	a6756223-a3fd-477a-a91e-05bd5dc1b56f	READ_SENTENCE_ORDER	连句成段		17
d558bccd-fcb2-4924-a3da-2c00d13acef8	8ca0dedb-466e-41aa-aa2f-2310853f499a	TRANSLATE_WORD_ORDER	翻译_连词成句		15
59f1ffbc-74f6-4f2d-910c-f0baa5c8f8aa	ab3645ad-52a1-4ae8-b728-7e748ee74271	SPEAK_FOLLOW	听音跟读		16
12b69f09-5355-426d-bffb-50a6c6355416	4da3d566-d428-4c13-8a1d-9acef5481fbd	STROKE_ORDER_WRITING	笔顺书写		17
