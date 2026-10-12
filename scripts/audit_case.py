#!/usr/bin/env python3
"""
Iran Legal Audit - Automated Legal Topic Scanner & Case Formatter
A lightweight CLI helper for formatting cases and cross-referencing statutory articles.
"""

import sys
import json
from pathlib import Path

STATUTES_INDEX = {
    "civil": [
        ("ماده ۱۰ قانون مدنی", "اصل آزادی اراده و نافذ بودن قراردادهای خصوصی"),
        ("ماده ۱۹۰ قانون مدنی", "شرایط اساسی صحت معامله: قصد، اهلیت، موضوع معین، مشروعیت جهت"),
        ("ماده ۲۱۹ قانون مدنی", "اصل لزوم قراردادها و عقود لازم"),
        ("ماده ۲۳۰ قانون مدنی", "وجه التزام قراردادی و عدم حق تعدیل دادگاه مگر مصوبات خاص"),
        ("ماده ۳۰۱ تا ۳۳۷ قانون مدنی", "ضمان قهری، غصب، اتلاف، تسبیب و استیفاء"),
    ],
    "commercial": [
        ("لایحه اصلاحی قانون تجارت ۱۳۴۷", "مقررات شرکت‌های سهامی، مجامع و حدود اختیارات مدیران"),
        ("ماده ۲۳ قانون صدور چک", "صدور مستقیم اجراییه دادگاه بدون نیاز به رسیدگی ماهوی"),
        ("ماده ۳۱۵ قانون تجارت", "مواعد واخواست و مسئولیت تضامنی ظهرنویسان"),
    ],
    "cyber_and_fata": [
        ("مواد ۱ تا ۳ قانون جرایم رایانه‌ای", "دسترسی غیرمجاز به سامانه‌ها یا داده‌های رایانه‌ای"),
        ("ماده ۱۳ قانون جرایم رایانه‌ای", "کلاهبرداری رایانه‌ای از طریق تغییر داده یا سامانه"),
        ("مواد ۱۶ تا ۱۸ قانون جرایم رایانه‌ای", "هتک حیثیت، نشر اکاذیب و انتشار صوت و تصویر خصوصی"),
        ("مواد ۳۲ و ۳۳ قانون جرایم رایانه‌ای", "الزام نگهداری ۶ ماهه داده‌های ترافیک توسط ISPها و هاستینگ‌ها"),
    ],
    "criminal": [
        ("ماده ۱ قانون تشدید مجازات", "کلاهبرداری و مانور متقلبانه برای بردن مال غیر"),
        ("ماده ۶۷۴ قانون مجازات اسلامی تعزیرات", "خیانت در امانت و تصاحب مال سپرده شده"),
        ("قانون کاهش مجازات حبس تعزیری ۱۳۹۹", "نصف شدن حبس‌ها و تبدیل کلاهبرداری زیر ۱۰۰ میلیون به قابل گذشت"),
    ],
    "labor_and_tax": [
        ("ماده ۱۴۸ قانون کار و ۳۶ تامین اجتماعی", "الزام کارفرما به پرداخت حق بیمه کارگر"),
        ("ماده ۱۰۵ قانون مالیات‌های مستقیم", "مالیات ۲۵ درصد بر عملکرد اشخاص حقوقی"),
        ("قانون پایانه‌های فروشگاهی و سامانه مودیان", "الزام صدور صورتحساب الکترونیکی در کارپوشه"),
    ],
}

def analyze_case_keywords(text: str) -> dict:
    """Scan case text and return relevant statutes and checklist flags."""
    matched = {}
    text_lower = text.lower()
    
    keywords_map = {
        "قرارداد": "civil",
        "وجه التزام": "civil",
        "فسخ": "civil",
        "چک": "commercial",
        "شرکت": "commercial",
        "فتا": "cyber_and_fata",
        "سایت": "cyber_and_fata",
        "پیج": "cyber_and_fata",
        "سیم‌کارت": "cyber_and_fata",
        "vpn": "cyber_and_fata",
        "کلاهبرداری": "criminal",
        "امانت": "criminal",
        "بیمه": "labor_and_tax",
        "کارگر": "labor_and_tax",
        "مالیات": "labor_and_tax",
    }
    
    for kw, cat in keywords_map.items():
        if kw in text_lower:
            matched.setdefault(cat, []).extend(STATUTES_INDEX.get(cat, []))
            
    # Deduplicate entries
    for cat in matched:
        matched[cat] = list(dict.fromkeys(matched[cat]))
        
    return matched

def format_case_template(topic: str) -> str:
    """Format dual-engine legal review framework."""
    # ponytail: [expanded web api] - add when full FastAPI server needed
    return f"""============================================================
پرونده حقوقی: {topic}
============================================================
۱. توصیف و تکییف حقوقی (Legal Qualification)
   - ماهیت رابطه یا واقعه حقوقی:
   - مرجع صالح رسیدگی (دادسرا / دادگاه حقوقی / شورا / اداره کار):
   - قوانین و مقررات حاکم:

۲. لایحه دفاعیه از منظر وکیل مدافع (Defense & Strategy)
   - ایرادات شکلی (ماده ۸۴ قانون آیین دادرسی مدنی):
   - دفاعیات ماهوی و تحلیل ادله اثبات:
   - استناد به اصول حقوقی، فقهی و آرای وحدت رویه:
   - تقاضای نهایی (رد دعوا / برائت / تقلیل خسارت):

۳. دادنامه و انشای رای از منظر قاضی دادگاه (Judicial Verdict)
   - گردش کار پرونده:
   - جهات و دلایل اثباتی محکمه:
   - تطبیق با مواد صریح قانون و آرا وحدت رویه:
   - منطوق دادنامه (حکم / قرار نهایی):

۴. چک‌لیست امن‌سازی و اقدامات فوری (Actionable Safeguards)
   - اصلاح شروط و ضمایم:
   - اقدامات پیشگیرانه انتظامی و مدارک مورد نیاز:
============================================================"""

def _test_self_check():
    """Runnable assert-based verification."""
    result = analyze_case_keywords("بررسی قرارداد سایت و کلاهبرداری اینترنتی")
    assert "civil" in result
    assert "cyber_and_fata" in result
    assert "criminal" in result
    tpl = format_case_template("تست")
    assert "توصیف و تکییف حقوقی" in tpl
    assert "لایحه دفاعیه" in tpl

if __name__ == "__main__":
    _test_self_check()
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        matches = analyze_case_keywords(query)
        print(format_case_template(query))
        print("\nقوانین و مستندات پیشنهادی مرتبط:")
        for cat, items in matches.items():
            print(f"\n[دسته {cat}]:")
            for article, desc in items:
                print(f"  - {article}: {desc}")
    else:
        print("Self-check passed. Pass case query to run CLI analysis.")
