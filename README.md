# Speech Signal Processing Project - صارحوني Analysis

<div dir="rtl">

# مشروع معالجة الإشارة الكلامية - تحليل كلمة "صارحوني"

</div>

## 📋 Project Overview / نظرة عامة على المشروع

This project implements speech signal processing techniques to analyze the Arabic word "صارحوني" using Python and Praat. It extracts acoustic features such as fundamental frequency, formant frequencies, and spectral characteristics.

<div dir="rtl">

هذا المشروع يطبق تقنيات معالجة الإشارة الصوتية لتحليل الكلمة العربية "صارحوني" باستخدام Python وبرنامج Praat. يتم استخراج الخصائص الصوتية مثل التردد الأساسي، ترددات البواني، والطيف الترددي.
</div>

## 🎯 Project Objectives / أهداف المشروع

- Record audio with specific parameters (16 kHz, 16-bit)
- Extract time windows for vowel sounds (Alif, Waw, Ya)
- Calculate fundamental frequency using two different methods
- Analyze frequency spectrum using FFT and LPC
- Extract formant frequencies (F1, F2, F3)
- Compare results with Praat software

<div dir="rtl">

- تسجيل الصوت بمواصفات محددة (16 kHz، 16-bit)
- استخراج نوافذ زمنية للأصوات المدية (الألف، الواو، الياء)
- حساب التردد الأساسي بطريقتين مختلفتين
- تحليل الطيف الترددي باستخدام FFT و LPC
- استخراج ترددات البواني (F1, F2, F3)
- المقارنة مع نتائج برنامج Praat
</div>

## 🛠️ Installation & Setup / التثبيت والإعداد

### Prerequisites / المتطلبات الأساسية

- Python 3.10 or higher
- Praat software (for comparison and verification)
- Microphone for recording

<div dir="rtl">

- Python 3.10 أو أعلى
- برنامج Praat (للمقارنة والتحقق)
- ميكروفون لل تسجيل
</div>

### Install Dependencies / تثبيت المكتبات المطلوبة

```bash
# Install required Python packages
pip install -r reqs.txt
```

Or install individually:

```bash
pip install numpy scipy librosa matplotlib sounddevice soundfile parselmouth
```

### Required Libraries / المكتبات المطلوبة

- **numpy**: Mathematical operations and arrays
- **scipy**: Signal processing and scientific functions
- **librosa**: Audio processing and analysis
- **matplotlib**: Plotting and visualization
- **sounddevice**: Audio recording
- **soundfile**: Audio file reading/writing
- **parselmouth**: Python interface for Praat

<div dir="rtl">

- **numpy**: العمليات الحسابية والمصفوفات
- **scipy**: معالجة الإشارة والدوال العلمية
- **librosa**: معالجة الصوت وتحليله
- **matplotlib**: الرسم البياني والتخيل
- **sounddevice**: تسجيل الصوت
- **soundfile**: قراءة وكتابة ملفات الصوت
- **parselmouth**: الواجهة البرمجية لبرنامج Praat
</div>

## ⚠️ Troubleshooting / استكشاف الأخطاء

### Common Issues / المشاكل الشائعة

1. **Microphone access denied**:
   - Check system permissions
   - Close other programs using microphone

2. **Library installation errors**:
   ```bash
   pip install --upgrade pip
   pip install wheel
   ```

4. **Praat errors**:
   - Ensure Praat is installed
   - Check paths in `parselmouth`

<div dir="rtl">
1. **لا يمكن الوصول إلى الميكروفون**:
   - تحقق من أذونات النظام
   - أغبق البرامج الأخرى التي تستخدم الميكروفون

2. **أخطاء في تثبيت المكتبات**:
   ```bash
   pip install --upgrade pip
   pip install wheel
   ```

3. **أخطاء في Praat**:

   - تأكد من تثبيت البرنامج
   - تحقق من المسارات في `parselmouth`
</div>

## 🤝 Contributing / المساهمة

To contribute to project development:
1. Fork the project
2. Create a new branch
3. Make your changes
4. Submit a pull request

<div dir="rtl">

للمساهمة في تطوير المشروع:
1. انسخ المشروع (Fork)
2. أنشئ فرعاً جديداً (Branch)
3. أضف التعديلات
4. أرسل طلب الدمج (Pull Request)
</div>


</div>

# 📊 Results & Analysis / النتائج والتحليل

## 🔗 Detailed Results / النتائج التفصيلية

For complete analysis results, charts, and detailed comparisons with Praat software, please refer to the dedicated results document:

**[📄 View Full Results Analysis](./results/ITE_ANL601_HW_F24_C2_ahmad_152818.md)**

<div dir="rtl">
للاطلاع على النتائج الكاملة، المخططات البيانية، والمقارنات التفصيلية مع برنامج Praat، يرجى الرجوع إلى وثيقة النتائج المخصصة:

**[📄 عرض تحليل النتائج الكامل](./results/ITE_ANL601_HW_F24_C2_ahmad_152818.md)**
</div>

## 📈 Key Findings / أبرز النتائج

The comprehensive analysis reveals important acoustic characteristics of the Arabic word "صارحوني" including:

- Fundamental frequency patterns across different vowels
- Formant transitions between phonemes
- Spectral properties and energy distribution
- Comparison between Python and Praat methodologies

<div dir="rtl">
يكشف التحليل الشامل عن الخصائص الصوتية المهمة للكلمة العربية "صارحوني" بما في ذلك:

- أنماط التردد الأساسي عبر الأصوات المديّة المختلفة
- انتقالات البواني بين الفونيمات
- الخصائص الطيفية وتوزيع الطاقة
- المقارنة بين منهجيات Python و Praat
</div>

## 📄 License / الترخيص

<div dir="rtl">
هذا المشروع مرخص تحت رخصة MIT. انظر ملف `LICENSE` للمزيد من التفاصيل.
</div>

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 👥 Authors / المؤلفون

- **Student**: ahmad ghassan deeb
- **Experinece**: senior python developer (+10 years)
- **Student ID**: 152818
- **Class**: C2
- **Semester**: F24
- **Course**: Natural Language Processing - NLP-ANL601
- **Professor**: Dr. Rwaad Melhem
- **Coordinator**: Dr. Oumayma Dakkak

<div dir="rtl">

- **الطالب**: أحمد غسان ديب
- **رقم الطالب**: 152818
- **الشعبة**: C2
- **الفصل**: F24
- **المقرر**: معالجة اللغات الطبيعية - NLP-ANL601
- **الأستاذ**: د. رواد ملحم
- **المنسق**: د. أميمة الدكاك

## 📞 Contact / معلومات التواصل

For inquiries or issue reporting:
- Email: ahmad_152818@svuonline.org
- Submission Date: 25-10-2025

<div dir="rtl">

للاستفسارات أو الإبلاغ عن مشاكل:
- البريد الإلكتروني: ahmad_152818@svuonline.org
- تاريخ التسليم: 25-10-2025
</div>

---