import React, { ReactElement } from 'react'

import SearchBar from 'components/SearchBar'

import { Container } from './style'

export default function Header(): ReactElement {
  return (
    <Container className="relative">
      <div className="absolute -bottom-6 w-full z-10 flex justify-center">
        <SearchBar />
      </div>
    </Container>
  )
}
