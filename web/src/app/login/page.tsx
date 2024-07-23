'use client'
import React, { useEffect, useState } from 'react'
import cn from 'classnames'
import Loading from '../components/base/loading'
import Forms from './forms'
import Header from './_header'
import style from './page.module.css'
import i18n from '@/i18n/i18next-config'

const SignIn = () => {
  const [loading, setLoading] = useState<boolean>(false)

  return (
    <>
      <div className={cn(
        style.background,
        'flex w-full min-h-screen',
        'sm:p-4 lg:p-8',
        'gap-x-20',
        'justify-center lg:justify-start',
      )}>
        <div className={
          cn(
            'flex w-full flex-col bg-white shadow rounded-2xl shrink-0',
            'space-between',
          )
        }>
          <Header />
          {loading && (
            <div className={
              cn(
                'flex flex-col items-center w-full grow justify-center',
                'px-6',
                'md:px-[108px]',
              )
            }>
              <Loading type='area' />
            </div>
          )}
          <>
            <Forms />
            <div className='px-8 py-6 text-sm font-normal text-gray-500'>
              © {new Date().getFullYear()} Vesnus, Inc. All rights reserved.
            </div>
          </>
        </div>

      </div>

    </>
  )
}

export default SignIn
