'use client'
import React, { useEffect, useReducer, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useRouter } from 'next/navigation'
import classNames from 'classnames'
import useSWR from 'swr'
import Link from 'next/link'
import Toast from '../components/base/toast'
import style from './page.module.css'
import { IS_CE_EDITION, apiPrefix } from '@/config'
import Button from '@/app/components/base/button'
import { login } from '@/service/common'
import { getPurifyHref } from '@/utils'
const validEmailReg = /^[\w\.-]+@([\w-]+\.)+[\w-]{2,}$/
import { LanguagesSupported } from '@/i18n/language'

type IState = {
  formValid: boolean
  github: boolean
  google: boolean
}

type IAction = {
  type: 'login' | 'login_failed' | 'github_login' | 'github_login_failed' | 'google_login' | 'google_login_failed'
}

function reducer(state: IState, action: IAction) {
  switch (action.type) {
    case 'login':
      return {
        ...state,
        formValid: true,
      }
    case 'login_failed':
      return {
        ...state,
        formValid: true,
      }
    case 'github_login':
      return {
        ...state,
        github: true,
      }
    case 'github_login_failed':
      return {
        ...state,
        github: false,
      }
    case 'google_login':
      return {
        ...state,
        google: true,
      }
    case 'google_login_failed':
      return {
        ...state,
        google: false,
      }
    default:
      throw new Error('Unknown action.')
  }
}

const NormalForm = () => {
  const { t } = useTranslation('login')

  const router = useRouter()

  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [isLoading, setIsLoading] = useState(false)
  const handleEmailPasswordLogin = async () => {
    if (!validEmailReg.test(email)) {
      Toast.notify({
        type: 'error',
        message: t('login.error.emailInValid'),
      })
      return
    }
    try {
      setIsLoading(true)
      const res = await login({
        url: '/login',
        body: {
          email,
          password,
          remember_me: true,
        },
      })
      console.log(res.data)
      // if (res.result === 'success') {
      //   console.log(res.data)
      //   localStorage.setItem('access_token', res.data)
      //   router.replace('/apps')
      // }
      // else {
      //   Toast.notify({
      //     type: 'error',
      //     message: res.data,
      //   })
      // }
    }
    finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <div className="w-full mx-auto">
        <h2 className="text-[32px] font-bold text-gray-900">{t('login.pageTitle')}</h2>
        <p className='mt-1 text-sm text-gray-600'>{t('login.welcome')}</p>
      </div>

      <div className="w-full mx-auto mt-8">
        <div className="bg-white ">
          {
              <form onSubmit={() => { }}>
                <div className='mb-5'>
                  <label htmlFor="email" className="my-2 block text-sm font-medium text-gray-900">
                    {t('login.email')}
                  </label>
                  <div className="mt-1">
                    <input
                      value={email}
                      onChange={e => setEmail(e.target.value)}
                      id="email"
                      type="email"
                      autoComplete="email"
                      placeholder={t('login.emailPlaceholder') || ''}
                      className={'appearance-none block w-full rounded-lg pl-[14px] px-3 py-2 border border-gray-200 hover:border-gray-300 hover:shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 placeholder-gray-400 caret-primary-600 sm:text-sm'}
                    />
                  </div>
                </div>

                <div className='mb-4'>
                  <label htmlFor="password" className="my-2 flex items-center justify-between text-sm font-medium text-gray-900">
                    <span>{t('login.password')}</span>
                  </label>
                  <div className="relative mt-1">
                    <input
                      id="password"
                      value={password}
                      onChange={e => setPassword(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter')
                          handleEmailPasswordLogin()
                      }}
                      type={showPassword ? 'text' : 'password'}
                      autoComplete="current-password"
                      placeholder={t('login.passwordPlaceholder') || ''}
                      className={'appearance-none block w-full rounded-lg pl-[14px] px-3 py-2 border border-gray-200 hover:border-gray-300 hover:shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 placeholder-gray-400 caret-primary-600 sm:text-sm pr-10'}
                    />
                    <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="text-gray-400 hover:text-gray-500 focus:outline-none focus:text-gray-500"
                      >
                        {showPassword ? '👀' : '😝'}
                      </button>
                    </div>
                  </div>
                </div>

                <div className='mb-2'>
                  <Button
                    tabIndex={0}
                    type='primary'
                    onClick={handleEmailPasswordLogin}
                    disabled={isLoading}
                    className="w-full !fone-medium !text-sm"
                  >{t('login.signBtn')}</Button>
                </div>
              </form>
          }
          {/*  agree to our Terms and Privacy Policy. */}
          <div className="w-hull text-center block mt-2 text-xs text-gray-600">
            {t('login.tosDesc')}
            &nbsp;
            <Link
              className='text-primary-600'
              target='_blank' rel='noopener noreferrer'
              href='https://dify.ai/terms'
            >{t('login.tos')}</Link>
            &nbsp;&&nbsp;
            <Link
              className='text-primary-600'
              target='_blank' rel='noopener noreferrer'
              href='https://dify.ai/privacy'
            >{t('login.pp')}</Link>
          </div>

          {IS_CE_EDITION && <div className="w-hull text-center block mt-2 text-xs text-gray-600">
            {t('login.goToInit')}
            &nbsp;
            <Link
              className='text-primary-600'
              href='/install'
            >{t('login.setAdminAccount')}</Link>
          </div>}

        </div>
      </div>
    </>
  )
}

export default NormalForm
