// Generate ambient Veo 3.1 clips for the homepage portfolio cards.
// Requires GEMINI_API_KEY in the environment (same Gemini API key used for
// Veo generation in noddak/coupon-book).
// Run: node store-assets/gen_veo.mjs [name|all]
import { writeFileSync, mkdirSync, existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = dirname(fileURLToPath(import.meta.url))
const OUT = join(ROOT, 'video')
mkdirSync(OUT, { recursive: true })

const BASE = 'https://generativelanguage.googleapis.com/v1beta'

const KEY = process.env.GEMINI_API_KEY
if (!KEY) {
  console.error('GEMINI_API_KEY is not set. Set it and re-run.')
  process.exit(1)
}

const STYLE =
  'Premium cinematic ambient loop, deep dark navy background, elegant, ' +
  'very slow subtle motion, soft depth of field, gentle floating light particles, ' +
  'no people, no readable text, no letters, no logos, no watermarks, no camera shake, ' +
  'seamless loopable motion.'

const CLIPS = {
  momoi: {
    file: 'momoi-raw.mp4',
    prompt: 'Abstract ambient loop: soft violet and purple sound waves flowing from a sleek dark smartphone silhouette, transforming into glowing calendar grid tiles and floating checkmark orbs drifting upward, ' + STYLE,
  },
  lecture: {
    file: 'lecture-raw.mp4',
    prompt: 'Abstract ambient loop: a glowing cyan audio waveform ribbon flowing into a floating holographic notebook page, where it becomes neat rows of abstract glowing dashes and highlighted blocks like summarized lecture notes, a soft light pen tip tracing lines, absolutely no musical notes, no musical notation, ' + STYLE,
  },
  songbit: {
    file: 'songbit-raw.mp4',
    prompt: 'Abstract ambient loop: neon pink and magenta equalizer bars pulsing very gently around a floating glowing vinyl disc, thin light trails orbiting like music staves, dreamy studio haze, ' + STYLE,
  },
  bible: {
    file: 'bible-raw.mp4',
    prompt: 'Abstract ambient loop: an open book made of soft mint and teal light floating in darkness, luminous particles rising from its pages like fireflies, warm gentle glow spreading, ' + STYLE,
  },
  coupon: {
    file: 'coupon-raw.mp4',
    prompt: 'Abstract ambient loop: glowing cyan ticket and coupon shapes with perforated edges floating and slowly rotating in dark space, one ticket gently flipping, soft light stamps appearing as small glowing circles, ' + STYLE,
  },
  receipt: {
    file: 'receipt-raw.mp4',
    prompt: 'Abstract ambient loop: a floating paper receipt silhouette being swept by a warm amber holographic scanning beam, glowing golden data particles lifting off the paper and forming a soft rising chart, ' + STYLE,
  },
}

async function generate(name, { file, prompt }) {
  const out = join(OUT, file)
  if (existsSync(out)) { console.log(`[${name}] exists, skip`); return }
  console.log(`[${name}] starting Veo 3.1 generation...`)
  const start = await fetch(`${BASE}/models/veo-3.1-generate-preview:predictLongRunning`, {
    method: 'POST',
    headers: { 'x-goog-api-key': KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      instances: [{ prompt }],
      parameters: { aspectRatio: '16:9', resolution: '720p' },
    }),
  })
  const startData = await start.json()
  if (!start.ok) throw new Error(`[${name}] start failed: ${JSON.stringify(startData.error || startData)}`)
  const op = startData.name
  console.log(`[${name}] operation: ${op}`)

  let uri = null
  for (let i = 0; i < 90; i++) {
    await new Promise(r => setTimeout(r, 10000))
    const st = await fetch(`${BASE}/${op}`, { headers: { 'x-goog-api-key': KEY } })
    const d = await st.json()
    if (d.error) throw new Error(`[${name}] poll error: ${JSON.stringify(d.error)}`)
    if (d.done) {
      uri = d.response?.generateVideoResponse?.generatedSamples?.[0]?.video?.uri
        || d.response?.generatedVideos?.[0]?.video?.uri
      if (!uri) throw new Error(`[${name}] done but no video uri: ${JSON.stringify(d.response || d).slice(0, 500)}`)
      break
    }
    console.log(`[${name}] waiting... ${(i + 1) * 10}s`)
  }
  if (!uri) throw new Error(`[${name}] timed out`)

  const dl = await fetch(uri, { headers: { 'x-goog-api-key': KEY }, redirect: 'follow' })
  if (!dl.ok) throw new Error(`[${name}] download failed: ${dl.status}`)
  const buf = Buffer.from(await dl.arrayBuffer())
  writeFileSync(out, buf)
  console.log(`[${name}] saved ${out} (${Math.round(buf.length / 1024)} KB)`)
}

const which = process.argv[2] || 'all'
const targets = which === 'all' ? Object.keys(CLIPS) : [which]
for (const t of targets) {
  if (!CLIPS[t]) throw new Error(`unknown clip: ${t}`)
  await generate(t, CLIPS[t])
}
console.log('done')
