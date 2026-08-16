import base64, json, urllib.request, os

URL = "https://echo.nanilpulse.art/api/voice"
HEADERS = {"Content-Type": "application/json", "Origin": "https://echo.nanilpulse.art"}
OUT = "assets/audio"

DEMOS = {
    "hoerbeispiel-grosshandel": {
        "EL": "Τέλεια — σημείωσα τα πάντα: 400 κιλά ντονέρ μοσχάρι σε σούβλες των 20 κιλών και 200 κιλά ντονέρ γαλοπούλα σε σούβλες των 15 κιλών, παράδοση την Πέμπτη στο Musterbetrieb Nord. Σύνολο 5.340 ευρώ καθαρά. Ένας γρήγορος έλεγχος: την προηγούμενη εβδομάδα η γαλοπούλα ήταν σε σούβλες των 20 κιλών — είναι σωστά τα 15 αυτή τη φορά; Η παραγγελία είναι έτοιμη και περιμένει την έγκρισή σας.",
        "RU": "Отлично — я всё записала: 400 килограммов дёнера из телятины на шампурах по 20 кило и 200 килограммов дёнера из индейки на шампурах по 15 кило, доставка в четверг в Musterbetrieb Nord. Итого 5 340 евро нетто. Одна быстрая проверка: на прошлой неделе индейка была на шампурах по 20 кило — в этот раз правильно 15? Заказ готов и ждёт вашего подтверждения.",
    },
    "voice-demo-gastro": {
        "EL": "Καλησπέρα σας, η Zeynah στο τηλέφωνο. Φυσικά — μια παραγγελία για παραλαβή: δύο ντονέρ με όλα, το ένα χωρίς κρεμμύδι, και δύο αϊράν. Παραλαβή στις 6:30 το απόγευμα. Σύνολο 24 ευρώ και 50 λεπτά. Τα σημείωσα όλα και τα έστειλα στην κουζίνα. Τα λέμε!",
        "RU": "Добрый день, это Zeynah. Конечно — заказ на вынос: два дёнера со всем, один без лука, и два айрана. Самовывоз в 18:30. Итого 24 евро 50. Я всё записала и передала на кухню. До встречи!",
    },
}

os.makedirs(OUT, exist_ok=True)
for name, langs in DEMOS.items():
    for lang, text in langs.items():
        out = os.path.join(OUT, f"{name}-{lang.lower()}.mp3")
        body = json.dumps({"text": text, "lang": lang}).encode()
        req = urllib.request.Request(URL, data=body, headers=HEADERS, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
        except Exception as e:
            print(f"FEHLER {out}: {e}")
            continue
        if "audio_base64" not in d:
            print(f"FEHLER {out}: {d}")
            continue
        with open(out, "wb") as f:
            f.write(base64.b64decode(d["audio_base64"]))
        print(f"OK {out} ({os.path.getsize(out)//1024} KB)")
