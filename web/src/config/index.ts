export let apiPrefix = ''

// NEXT_PUBLIC_API_PREFIX=/console/api NEXT_PUBLIC_PUBLIC_API_PREFIX=/api npm run start
if (process.env.NEXT_PUBLIC_API_PREFIX) {
  apiPrefix = process.env.NEXT_PUBLIC_API_PREFIX
}
else if (
  globalThis.document?.body?.getAttribute('data-api-prefix')
) {
  // Not build can not get env from process.env.NEXT_PUBLIC_ in browser https://nextjs.org/docs/basic-features/environment-variables#exposing-environment-variables-to-the-browser
  apiPrefix = globalThis.document.body.getAttribute('data-api-prefix') as string
}
else {
  // const domainParts = globalThis.location?.host?.split('.');
  // in production env, the host is dify.app . In other env, the host is [dev].dify.app
  // const env = domainParts.length === 2 ? 'ai' : domainParts?.[0];
  apiPrefix = 'http://localhost:5001/api'
}

export const API_PREFIX: string = apiPrefix

const EDITION = process.env.NEXT_PUBLIC_EDITION || globalThis.document?.body?.getAttribute('data-public-edition') || 'SELF_HOSTED'
export const IS_CE_EDITION = EDITION === 'SELF_HOSTED'

export const LOCALE_COOKIE_NAME = 'locale'