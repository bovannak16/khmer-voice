# Khmer Voice Studio

Web App បម្លែងអត្ថបទខ្មែរជាសំឡេង (ប្រុស: Piseth / ស្រី: Sreymom) ទាញយក MP3 និង WAV។

## ដំណើរការលើកុំព្យូទ័រ
```
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
```
បើកកម្មវិធីរុករក៖ http://localhost:8000

## របៀបប្រើ
- សរសេរ `ប្រុស:` ឬ `ស្រី:` នៅដើមបន្ទាត់ ដើម្បីជ្រើសអ្នកនិយាយ
- ជ្រើសម៉ូដ Podcast / អាជីវកម្ម / និទានរឿង / សន្ទនា
- កែល្បឿន កម្រិតសំឡេង និងចន្លោះរវាងប្រយោគ ហើយចុច "បង្កើតសំឡេង"

## Deploy លើអ៊ីនធឺណិត
ត្រូវការ server ដែលដំណើរការ Python (Render, Railway, Fly.io, VPS)។
Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
(Cloudflare Workers មិនគាំទ្រ Python/edge-tts ដោយផ្ទាល់ទេ។)

## ចំណាំ
Server ត្រូវការអ៊ីនធឺណិតដើម្បីហៅសេវា TTS របស់ Microsoft Edge (តាមរយៈ edge-tts)។
