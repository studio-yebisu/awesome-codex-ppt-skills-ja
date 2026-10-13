/**
 * 영상 넣기 안내(사용자 요청 10-08): 스톡 영상 검색·다운로드를 자동화하려면 사용자가 직접 API 키를 발급하도록 권한다.
 * 키는 레포에 넣지 않는다 — .env(.gitignore)나 셸 환경변수로만. `npm run check`의 secrets 검사가 커밋을 막는다.
 */
export const MEDIA_KEY_VARS = ['PEXELS_API_KEY', 'PIXABAY_API_KEY'];

export function mediaNotice(env = process.env) {
  if (MEDIA_KEY_VARS.some((k) => env[k])) return null;
  return [
    '[알림] 영상 넣기 — 스톡 영상을 자동으로 찾아 받으려면 API 키를 직접 발급해 두길 권장합니다.',
    '  · Pexels  https://www.pexels.com/api/   → PEXELS_API_KEY',
    '  · Pixabay https://pixabay.com/api/docs/ → PIXABAY_API_KEY',
    '  · 키는 프로젝트 루트 .env 또는 셸 환경변수에만 두세요. .env는 .gitignore에 있고, `npm run check`가 키 커밋을 막습니다.',
    '  · 키 없이도 직접 찍은 영상·직접 받은 무료 영상(라이선스·출처는 decks/<id>/assets/CREDITS.md)으로 넣을 수 있습니다.',
  ].join('\n');
}

export function printMediaNotice(env = process.env, log = console.error) {
  const text = mediaNotice(env);
  if (text) log(text);
  return Boolean(text);
}
