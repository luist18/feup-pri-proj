import type { AppProps } from 'next/app'

import 'normalize.css'
import 'styles/globals.css'

import SearchProvider from 'context/search'

const MyApp = ({ Component, pageProps }: AppProps) => (
  <SearchProvider>
    <Component {...pageProps} />
  </SearchProvider>
)

export default MyApp
