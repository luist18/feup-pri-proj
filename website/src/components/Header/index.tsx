import React, { ReactElement } from 'react'

import SearchBar from 'components/SearchBar'

import { Container } from './style'

export default function Header(): ReactElement {
  return (
    <Container>
      <SearchBar />
    </Container>
  )
}
