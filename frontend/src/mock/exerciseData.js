// Mock 数据 - 符合数据库结构设计

// Content System Mock 数据
export const contentSystemMock = {
  // 技能大类
  skillCategories: [
    { id: '1', name: 'listening', description: '听力技能', display_order: 1 },
    { id: '2', name: 'speaking', description: '口语技能', display_order: 2 },
    { id: '3', name: 'reading', description: '阅读技能', display_order: 3 },
    { id: '4', name: 'writing', description: '写作技能', display_order: 4 }
  ],

  // 题型定义
  exerciseTypes: [
    { id: 'et1', skill_category_id: '1', name: 'listen_and_choose_image', display_name: '听音选图', description: '听音频选择对应图片', display_order: 1 },
    { id: 'et2', skill_category_id: '1', name: 'listen_and_judge', display_name: '听音判断', description: '听音频判断正误', display_order: 2 },
    { id: 'et3', skill_category_id: '2', name: 'read_aloud', display_name: '朗读句子', description: '朗读给定句子', display_order: 1 },
    { id: 'et4', skill_category_id: '3', name: 'reading_comprehension', display_name: '阅读理解', description: '阅读文章回答问题', display_order: 1 },
    { id: 'et5', skill_category_id: '4', name: 'fill_in_blank', display_name: '填空题', description: '根据提示填写汉字', display_order: 1 }
  ],

  // 媒体资产
  mediaAssets: [
    { id: 'ma1', file_url: 'https://example.com/audio/hello.mp3', file_type: 'audio', mime_type: 'audio/mp3', description: '你好发音', created_at: '2024-01-15T10:00:00Z' },
    { id: 'ma2', file_url: 'https://example.com/images/apple.jpg', file_type: 'image', mime_type: 'image/jpeg', description: '苹果图片', created_at: '2024-01-15T10:05:00Z' },
    { id: 'ma3', file_url: 'https://example.com/audio/sentence1.mp3', file_type: 'audio', mime_type: 'audio/mp3', description: '句子朗读', created_at: '2024-01-16T09:00:00Z' }
  ],

  // 题目
  exercises: [
    {
      id: 'ex1',
      parent_exercise_id: null,
      exercise_type_id: 'et1',
      word_id: 'w1',
      prompt: '听音频，选择正确的图片',
      metadata: {
        options: [
          { key: 'A', image_url: 'https://example.com/images/apple.jpg', text: '苹果' },
          { key: 'B', image_url: 'https://example.com/images/banana.jpg', text: '香蕉' },
          { key: 'C', image_url: 'https://example.com/images/orange.jpg', text: '橙子' }
        ],
        correct_answer: 'A'
      },
      difficulty_level: 1,
      quality_status: 1,
      created_by: 'admin',
      created_at: '2024-01-15T10:00:00Z'
    },
    {
      id: 'ex2',
      parent_exercise_id: null,
      exercise_type_id: 'et2',
      word_id: 'w2',
      prompt: '听音频，判断句子是否正确',
      metadata: {
        audio_text: '今天天气很好',
        correct_answer: true
      },
      difficulty_level: 1,
      quality_status: 1,
      created_by: 'teacher1',
      created_at: '2024-01-16T11:00:00Z'
    },
    {
      id: 'ex3',
      parent_exercise_id: null,
      exercise_type_id: 'et4',
      word_id: null,
      prompt: '阅读下面的文章，回答问题',
      metadata: {
        passage: '小明是一个学生。他每天早上七点起床，八点去学校。他喜欢学习汉语。',
        questions: [
          {
            question: '小明几点起床？',
            options: ['六点', '七点', '八点'],
            correct_answer: '七点'
          }
        ]
      },
      difficulty_level: 2,
      quality_status: 1,
      created_by: 'admin',
      created_at: '2024-01-17T14:00:00Z'
    },
    {
      id: 'ex4',
      parent_exercise_id: null,
      exercise_type_id: 'et5',
      word_id: 'w3',
      prompt: '请填写正确的汉字：我___学习汉语',
      metadata: {
        blanks: [
          { position: 1, correct_answer: '在', hints: '表示正在进行' }
        ]
      },
      difficulty_level: 1,
      quality_status: 0,
      created_by: 'teacher2',
      created_at: '2024-01-18T09:30:00Z'
    },
    {
      id: 'ex5',
      parent_exercise_id: null,
      exercise_type_id: 'et3',
      word_id: 'w4',
      prompt: '请朗读下面的句子',
      metadata: {
        sentence: '你好，很高兴认识你。',
        pronunciation_tips: '注意"认识"的发音'
      },
      difficulty_level: 2,
      quality_status: 1,
      created_by: 'teacher1',
      created_at: '2024-01-19T10:00:00Z'
    }
  ],

  // 题目媒体关联
  exerciseMediaAssets: [
    { exercise_id: 'ex1', media_asset_id: 'ma1', usage_role: 'prompt_audio' },
    { exercise_id: 'ex1', media_asset_id: 'ma2', usage_role: 'option_image' },
    { exercise_id: 'ex2', media_asset_id: 'ma3', usage_role: 'prompt_audio' }
  ],

  // 单词表
  words: [
    { id: 'w1', characters: '苹果', pinyin: 'píngguǒ', translation: 'apple', hsk_level: 1, audio_url: 'https://example.com/audio/pingguo.mp3' },
    { id: 'w2', characters: '天气', pinyin: 'tiānqì', translation: 'weather', hsk_level: 1, audio_url: 'https://example.com/audio/tianqi.mp3' },
    { id: 'w3', characters: '在', pinyin: 'zài', translation: 'at/in/on', hsk_level: 1, audio_url: 'https://example.com/audio/zai.mp3' },
    { id: 'w4', characters: '认识', pinyin: 'rènshi', translation: 'to know/recognize', hsk_level: 2, audio_url: 'https://example.com/audio/renshi.mp3' }
  ]
}

// Scenario Learning System Mock 数据
export const scenarioSystemMock = {
  // 情境技能分类
  slSkillCategories: [
    { id: 'sc1', name: 'listening', description: '听力理解' },
    { id: 'sc2', name: 'reading', description: '阅读理解' },
    { id: 'sc3', name: 'speaking', description: '口语表达' },
    { id: 'sc4', name: 'writing', description: '写作能力' }
  ],

  // 情境题型定义
  slExerciseTypes: [
    { id: 'set1', name: 'ai_generated_choice', skill_category_id: 'sc1', display_order: 1 },
    { id: 'set2', name: 'ai_generated_comprehension', skill_category_id: 'sc2', display_order: 1 },
    { id: 'set3', name: 'ai_generated_dialogue', skill_category_id: 'sc3', display_order: 1 }
  ],

  // 生成任务/主题
  topics: [
    { topic_id: 1, topic_name: '餐厅点餐', input_hsk_level: 2, job_id: 'job_001', stage2_input: {}, user_id: 'user1', created_at: '2024-01-20T10:00:00Z' },
    { topic_id: 2, topic_name: '购物场景', input_hsk_level: 3, job_id: 'job_002', stage2_input: {}, user_id: 'user1', created_at: '2024-01-21T11:00:00Z' }
  ],

  // 生成课程
  generatedLessons: [
    {
      lesson_db_id: 1,
      topic_id: 1,
      lesson_name: '在餐厅点餐',
      type: 'dialogue',
      passage: null,
      lesson_id_str: 'lesson_restaurant_001',
      generated_at: '2024-01-20T10:30:00Z'
    },
    {
      lesson_db_id: 2,
      topic_id: 2,
      lesson_name: '超市购物',
      type: 'passage',
      passage: {
        paragraphs: [
          '今天是周末，小李去超市买东西。',
          '超市里有很多人。小李买了一些水果和蔬菜。',
          '他还买了一瓶牛奶。最后，他在收银台付钱。'
        ]
      },
      lesson_id_str: 'lesson_shopping_001',
      generated_at: '2024-01-21T11:30:00Z'
    }
  ],

  // 对话内容
  dialogues: [
    {
      dialogue_id: 1,
      lesson_db_id: 1,
      roles: { A: '服务员', B: '顾客' },
      dialogues: [
        { role: 'A', text: '您好，请问您想吃什么？' },
        { role: 'B', text: '我想要一碗面条。' },
        { role: 'A', text: '好的，您要什么口味的？' },
        { role: 'B', text: '牛肉面，谢谢。' }
      ]
    }
  ],

  // 词汇库
  vocabulary: [
    { vocab_uuid: 'v1', word: '餐厅', hsk_level: 2, pinyin: 'cāntīng', translation: 'restaurant' },
    { vocab_uuid: 'v2', word: '点餐', hsk_level: 2, pinyin: 'diǎncān', translation: 'order food' },
    { vocab_uuid: 'v3', word: '超市', hsk_level: 2, pinyin: 'chāoshì', translation: 'supermarket' },
    { vocab_uuid: 'v4', word: '收银台', hsk_level: 3, pinyin: 'shōuyíntái', translation: 'cashier' }
  ],

  // 课程词汇包
  generatedVocabPackages: [
    { vocab_package_db_id: 1, lesson_db_id: 1, vocab_uuid: 'v1' },
    { vocab_package_db_id: 2, lesson_db_id: 1, vocab_uuid: 'v2' },
    { vocab_package_db_id: 3, lesson_db_id: 2, vocab_uuid: 'v3' },
    { vocab_package_db_id: 4, lesson_db_id: 2, vocab_uuid: 'v4' }
  ],

  // 情境练习
  slExercises: [
    {
      id: 'slex1',
      source_lesson_db_id: 1,
      vocab_package_db_id: 1,
      parent_exercise_id: null,
      exercise_type_id: 'set1',
      metadata: {
        question: '在对话中，顾客想吃什么？',
        options: ['米饭', '面条', '饺子', '包子'],
        correct_answer: '面条',
        explanation: 'AI生成：顾客说"我想要一碗面条"'
      },
      difficulty_level: 2,
      created_by: 'ai_system',
      created_at: '2024-01-20T11:00:00Z'
    },
    {
      id: 'slex2',
      source_lesson_db_id: 2,
      vocab_package_db_id: 3,
      parent_exercise_id: null,
      exercise_type_id: 'set2',
      metadata: {
        question: '小李在哪里买东西？',
        options: ['商店', '超市', '市场', '餐厅'],
        correct_answer: '超市',
        explanation: 'AI生成：文章开头提到"小李去超市买东西"'
      },
      difficulty_level: 2,
      created_by: 'ai_system',
      created_at: '2024-01-21T12:00:00Z'
    },
    {
      id: 'slex3',
      source_lesson_db_id: 1,
      vocab_package_db_id: 2,
      parent_exercise_id: null,
      exercise_type_id: 'set3',
      metadata: {
        prompt: '请根据对话场景，用"点餐"造一个句子',
        sample_answer: '我在餐厅点餐的时候，服务员很热情。',
        evaluation_criteria: ['使用了"点餐"词汇', '句子通顺', '符合场景']
      },
      difficulty_level: 3,
      created_by: 'ai_system',
      created_at: '2024-01-20T11:30:00Z'
    }
  ],

  // 情境媒体资产
  slMediaAssets: [
    { id: 'slma1', file_url: 'https://example.com/ai/audio/dialogue_restaurant.mp3', file_type: 'audio', mime_type: 'audio/mp3' },
    { id: 'slma2', file_url: 'https://example.com/ai/audio/passage_shopping.mp3', file_type: 'audio', mime_type: 'audio/mp3' }
  ],

  // 练习媒体关联
  slExerciseMediaAssets: [
    { exercise_id: 'slex1', media_asset_id: 'slma1', usage_role: 'prompt_audio' },
    { exercise_id: 'slex2', media_asset_id: 'slma2', usage_role: 'prompt_audio' }
  ]
}
