import {API_PREFIX} from '@/config'
import Toast from '@/app/components/base/toast'


const TIME_OUT = 100000
const ContentType = {
    json: 'application/json',
    stream: 'text/event-stream',
    form: 'application/x-www-form-urlencoded; charset=UTF-8',
    download: 'application/octet-stream', // for download
    upload: 'multipart/form-data', // for upload
  }
const baseOptions = {
    method: 'GET',
    mode: 'cors',
    credentials: 'include', // always send cookies、HTTP Basic authentication.
    headers: new Headers({
      'Content-Type': ContentType.json,
    }),
    redirect: 'follow',
  }

type FetchOptionType = Omit<RequestInit, 'body'> & {
    params?: Record<string, any>
    body?: BodyInit | Record<string, any> | null
}

export type IOtherOptions = {
    bodyStringify?: boolean
    silent?: boolean
}

const baseFetch = <T>(
    url: string,
    fetchOptions: FetchOptionType,
    {
        bodyStringify = true,
        silent,
    }: IOtherOptions,
  ): Promise<T> => {
    const options: typeof baseOptions & FetchOptionType = Object.assign({}, baseOptions, fetchOptions)
    const accessToken = localStorage.getItem('token')
    options.headers.set('Authorization', `Bearer ${accessToken}`)
    const contentType = options.headers.get('Content-Type')
    if (!contentType)
    options.headers.set('Content-Type', ContentType.json)
  
    const urlPrefix = API_PREFIX
    let urlWithPrefix = `${urlPrefix}${url.startsWith('/') ? url : `/${url}`}`
  
    const { method, params, body } = options
    // handle query
    if (method === 'GET' && params) {
      const paramsArray: string[] = []
      Object.keys(params).forEach(key =>
        paramsArray.push(`${key}=${encodeURIComponent(params[key])}`),
      )
      if (urlWithPrefix.search(/\?/) === -1)
        urlWithPrefix += `?${paramsArray.join('&')}`
  
      else
        urlWithPrefix += `&${paramsArray.join('&')}`
  
      delete options.params
    }
  
    if (body && bodyStringify)
      options.body = JSON.stringify(body)
  
    // Handle timeout
    return Promise.race([
      new Promise((resolve, reject) => {
        setTimeout(() => {
          reject(new Error('request timeout'))
        }, TIME_OUT)
      }),
      new Promise((resolve, reject) => {
        globalThis.fetch(urlWithPrefix, options as RequestInit)
          .then((res) => {
            const resClone = res.clone()
            // Error handler
            if (!/^(2|3)\d{2}$/.test(String(res.status))) {
              const bodyJson = res.json()
              switch (res.status) {
                case 401: {
                  console.log("fetch code 401", urlWithPrefix)
                  break
                }
                case 403:
                    console.log("fetch code 401", urlWithPrefix)
                  break
                // fall through
                default:
                  console.log("unhandle error code", res.status, urlWithPrefix)
              }
              return Promise.reject(resClone)
            }
  
            // handle delete api. Delete api not return content.
            if (res.status === 204) {
              resolve({ result: 'success' })
              return
            }
  
            // return data
            const data: Promise<T> = options.headers.get('Content-type') === ContentType.download ? res.blob() : res.json()
            resolve(data)
          })
          .catch((err) => {
            if (!silent)
              Toast.notify({ type: 'error', message: err })
            reject(err)
          })
      }),
    ]) as Promise<T>
}

// base request
export const request = <T>(url: string, options = {}, otherOptions?: IOtherOptions) => {
    return baseFetch<T>(url, options, otherOptions || {})
}

// request methods
export const get = <T>(url: string, options = {}, otherOptions?: IOtherOptions) => {
    return request<T>(url, Object.assign({}, options, { method: 'GET' }), otherOptions)
}

export const post = <T>(url: string, options = {}, otherOptions?: IOtherOptions) => {
    return request<T>(url, Object.assign({}, options, { method: 'POST' }), otherOptions)
}
