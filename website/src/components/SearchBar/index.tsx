import React, { ReactElement } from 'react'
import { Container } from './style'

export default function SearchBar(): ReactElement {
  return (
    <Container>
      <input type="text" placeholder="Search" />
    </Container>
  )
}
