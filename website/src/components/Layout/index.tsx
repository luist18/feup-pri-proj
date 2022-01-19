import React, { ReactElement, ReactNode } from 'react'

import { Container } from './style'

interface Props {
  children?: ReactNode
}

export default function Layout({ children }: Props): ReactElement {
  return <Container>{children}</Container>
}

Layout.defaultProps = {
  children: undefined,
}
