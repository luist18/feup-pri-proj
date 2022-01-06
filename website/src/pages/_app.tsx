import type { AppProps } from 'next/app'
import 'normalize.css'

import '../styles/globals.css'

const MyApp = ({ Component, pageProps }: AppProps) => <Component {...pageProps} />

export default MyApp
