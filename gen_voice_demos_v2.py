# -*- coding: utf-8 -*-
"""Neue Grosshandel-Voice-Demos v2: Telefon-Bestellung + WhatsApp-Sprachnachricht, 6 Sprachen."""
import base64, json, urllib.request, os, sys

URL = "https://echo.nanilpulse.art/api/voice"
HEADERS = {"Content-Type": "application/json", "Origin": "https://echo.nanilpulse.art"}
OUT = "assets/audio"

DEMOS = {
    "hoerbeispiel-grosshandel": {
        "DE": "Guten Tag, hier ist Zeynah, die digitale Assistentin von FrischeGross Weber. Alles klar — ich habe alles notiert: 400 Kilo Kalbdöner auf 20-Kilo-Spießen und 200 Kilo Putendöner auf 15-Kilo-Spießen, Lieferung Donnerstag an den Musterbetrieb Nord. Das macht 5.340 Euro netto. Eine kurze Prüfung: letzte Woche war die Pute auf 20-Kilo-Spießen — stimmen diesmal 15? Die Bestellung liegt zur Freigabe bereit.",
        "TR": "İyi günler, ben Zeynah, FrischeGross Weber'in dijital asistanı. Tamam, her şeyi not aldım: 20 kiloluk şişlerde 400 kilo dana döner ve 15 kiloluk şişlerde 200 kilo hindi döner, perşembe günü Musterbetrieb Nord'a teslimat. Toplam 5.340 euro artı KDV. Bir şeyi kontrol edeyim: geçen hafta hindi 20 kiloluk şişti — bu sefer gerçekten 15 kilo mu olsun? Sipariş hazır, onayınızı bekliyor.",
        "EN": "Good afternoon, this is Zeynah, the digital assistant of FrischeGross Weber. Got it — I've noted everything: 400 kilos of veal döner on 20-kilo skewers and 200 kilos of turkey döner on 15-kilo skewers, delivery Thursday to Musterbetrieb Nord. That comes to 5,340 euros net. One quick check: last week the turkey was on 20-kilo skewers — is 15 correct this time? The order is ready and waiting for your approval.",
        "AR": "مساء الخير، معك زينة، المساعدة الرقمية لشركة فريشه غروس فيبر. تمام، سجلت كل شيء: 400 كيلو دونر عجل على أسياخ 20 كيلو و200 كيلو دونر ديك رومي على أسياخ 15 كيلو، التوصيل يوم الخميس إلى موستربيتريب نورد. المجموع 5,340 يورو صافي. سؤال سريع: الأسبوع الماضي كان الديك الرومي بأسياخ 20 كيلو — هل 15 صحيح هذه المرة؟ الطلب جاهز وينتظر موافقتك.",
        "EL": "Καλησπέρα σας, είμαι η Zeynah, η ψηφιακή βοηθός της FrischeGross Weber. Τέλεια — σημείωσα τα πάντα: 400 κιλά ντονέρ μοσχάρι σε σούβλες των 20 κιλών και 200 κιλά ντονέρ γαλοπούλα σε σούβλες των 15 κιλών, παράδοση την Πέμπτη στο Musterbetrieb Nord. Σύνολο 5.340 ευρώ καθαρά. Ένας γρήγορος έλεγχος: την προηγούμενη εβδομάδα η γαλοπούλα ήταν σε σούβλες των 20 κιλών — είναι σωστά τα 15 αυτή τη φορά; Η παραγγελία είναι έτοιμη και περιμένει την έγκρισή σας.",
        "RU": "Добрый день, это Zeynah, цифровой ассистент компании FrischeGross Weber. Отлично — я всё записала: 400 килограммов дёнера из телятины на шампурах по 20 кило и 200 килограммов дёнера из индейки на шампурах по 15 кило, доставка в четверг в Musterbetrieb Nord. Итого 5 340 евро нетто. Одна быстрая проверка: на прошлой неделе индейка была на шампурах по 20 кило — в этот раз правильно 15? Заказ готов и ждёт вашего подтверждения.",
    },
    "voice-demo-grosshandel": {
        "DE": "Danke für Ihre Sprachnachricht! Ich habe alles erfasst: 20 Kisten Tomaten, 10 Säcke Kartoffeln, dazu 50 Liter Milch mit 3,5 Prozent Fett — Lieferung morgen früh vor 7 Uhr. Einen Wunsch habe ich mitgeschrieben: bitte reife Tomaten für den Wochenmarkt. Die Bestellung liegt jetzt bei Herrn Weber zur Freigabe. Sie bekommen gleich eine schriftliche Bestätigung hier in WhatsApp.",
        "TR": "Sesli mesajınız için teşekkürler! Her şeyi kaydettim: 20 kasa domates, 10 çuval patates, ayrıca yüzde 3,5 yağlı 50 litre süt — teslimat yarın sabah saat 7'den önce. Bir isteğinizi de not ettim: lütfen pazar için olgun domatesler. Sipariş şimdi Bay Weber'in onayında. Az sonra buradan, WhatsApp üzerinden yazılı onay alacaksınız.",
        "EN": "Thank you for your voice message! I've captured everything: 20 crates of tomatoes, 10 sacks of potatoes, plus 50 litres of milk at 3.5 percent fat — delivery tomorrow morning before 7 am. I also noted your request: ripe tomatoes for the weekly market, please. The order is now with Mr Weber for approval. You'll receive a written confirmation right here in WhatsApp.",
        "AR": "شكراً لرسالتك الصوتية! سجلت كل شيء: 20 صندوق طماطم، 10 أكياس بطاطس، إضافة إلى 50 لتر حليب بدهن 3,5 بالمئة — التوصيل غداً صباحاً قبل الساعة السابعة. ودوّنت طلبك أيضاً: طماطم ناضجة للسوق الأسبوعي من فضلك. الطلب الآن لدى السيد فيبر للموافقة. ستصلك رسالة تأكيد مكتوبة هنا في واتساب بعد قليل.",
        "EL": "Ευχαριστούμε για το φωνητικό σας μήνυμα! Τα κατέγραψα όλα: 20 κιβώτια ντομάτες, 10 σάκοι πατάτες, συν 50 λίτρα γάλα με 3,5 τοις εκατό λιπαρά — παράδοση αύριο το πρωί πριν τις 7. Σημείωσα και την επιθυμία σας: ώριμες ντομάτες για τη λαϊκή αγορά, παρακαλώ. Η παραγγελία βρίσκεται τώρα στον κ. Weber προς έγκριση. Θα λάβετε γραπτή επιβεβαίωση εδώ στο WhatsApp.",
        "RU": "Спасибо за ваше голосовое сообщение! Я всё записала: 20 ящиков томатов, 10 мешков картофеля, а также 50 литров молока жирностью 3,5 процента — доставка завтра утром до 7 часов. Я также отметила ваше пожелание: спелые томаты для рынка, пожалуйста. Заказ сейчас у господина Вебера на подтверждении. Вы получите письменное подтверждение прямо здесь, в WhatsApp.",
    },
}

os.makedirs(OUT, exist_ok=True)
fails = 0
for name, langs in DEMOS.items():
    for lang, text in langs.items():
        out = os.path.join(OUT, f"{name}-{lang.lower()}.mp3")
        body = json.dumps({"text": text, "lang": lang}).encode()
        req = urllib.request.Request(URL, data=body, headers=HEADERS, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
        except Exception as e:
            print(f"FEHLER {out}: {e}"); fails += 1; continue
        if "audio_base64" not in d:
            print(f"FEHLER {out}: {d}"); fails += 1; continue
        data = base64.b64decode(d["audio_base64"])
        if not data.startswith(b"ID3") and not data.startswith(b"\xff"):
            print(f"FEHLER {out}: kein MP3-Magic"); fails += 1; continue
        with open(out, "wb") as f:
            f.write(data)
        print(f"OK {out} ({len(data)//1024} KB)")
print("FERTIG" if fails == 0 else f"{fails} FEHLER")
sys.exit(1 if fails else 0)
