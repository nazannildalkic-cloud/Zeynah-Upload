import base64, json, urllib.request, os

URL = "https://echo.nanilpulse.art/api/voice"
HEADERS = {"Content-Type": "application/json", "Origin": "https://echo.nanilpulse.art"}
OUT = "assets/audio"

DEMOS = {
    "hoerbeispiel-grosshandel": {
        "EN": "Got it — I've noted everything: 400 kilos of veal döner on 20-kilo skewers and 200 kilos of turkey döner on 15-kilo skewers, delivery Thursday to Musterbetrieb Nord. That comes to 5,340 euros net. One quick check: last week the turkey was 20-kilo skewers — is 15 correct this time? The order is ready and waiting for your approval.",
        "TR": "Tamam, her şeyi not aldım: 20 kiloluk şişlerde 400 kilo dana döner ve 15 kiloluk şişlerde 200 kilo hindi döner, perşembe günü Musterbetrieb Nord'a teslimat. Toplam 5.340 euro artı KDV. Bir şeyi kontrol edeyim: geçen hafta hindi 20 kiloluk şişti — bu sefer gerçekten 15 kilo mu olsun? Sipariş hazır, onayınızı bekliyor.",
        "AR": "تمام، سجلت كل شيء: 400 كيلو دونر عجل على أسياخ 20 كيلو و200 كيلو دونر ديك رومي على أسياخ 15 كيلو، التوصيل يوم الخميس إلى موستربيتريب نورد. المجموع 5,340 يورو صافي. سؤال سريع: الأسبوع الماضي كان الديك الرومي بأسياخ 20 كيلو — هل 15 صحيح هذه المرة؟ الطلب جاهز وينتظر موافقتك.",
    },
    "voice-demo-gastro": {
        "EN": "Good afternoon, Zeynah speaking. Of course — a pickup order: two döner with everything, one without onions, plus two ayran. Pickup at 6:30 pm. That's 24 euros 50 in total. I've noted everything and sent it to the kitchen. See you later!",
        "TR": "İyi günler, ben Zeynah. Tabii — gel-al siparişi: iki döner her şey dahil, biri soğansız, yanına iki ayran. Teslim alma saati 18:30. Toplam 24 euro 50. Her şeyi not aldım ve mutfağa ilettim. Görüşmek üzere!",
        "AR": "مساء الخير، معك زينة. طبعاً — طلب استلام: اثنان دونر بكل شيء، واحد بدون بصل، مع اثنين عيران. الاستلام الساعة 6:30 مساءً. المجموع 24 يورو و50 سنت. سجلت كل شيء وأرسلته إلى المطبخ. إلى اللقاء!",
    },
}

os.makedirs(OUT, exist_ok=True)
for name, langs in DEMOS.items():
    for lang, text in langs.items():
        out = os.path.join(OUT, f"{name}-{lang.lower()}.mp3")
        body = json.dumps({"text": text, "lang": lang}).encode()
        req = urllib.request.Request(URL, data=body, headers=HEADERS, method="POST")
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.load(r)
        if "audio_base64" not in d:
            print(f"FEHLER {out}: {d}")
            continue
        with open(out, "wb") as f:
            f.write(base64.b64decode(d["audio_base64"]))
        print(f"OK {out} ({os.path.getsize(out)//1024} KB)")
