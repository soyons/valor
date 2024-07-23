import { get, post } from './base'
import type { Fetcher } from 'swr'
import {
  CommonResponse
} from '@/models/common'

export const login: Fetcher<CommonResponse & { data: string }, { url: string; body: Record<string, any> }> = ({ url, body }) => {
  return post(url, { body }, ) as Promise<CommonResponse & { data: string }>
}