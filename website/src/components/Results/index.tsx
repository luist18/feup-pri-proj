import React, { ReactElement } from 'react'

import { useSearch } from 'context/search'

import { Container } from './style'

export default function Results(): ReactElement {
  const { state } = useSearch()

  return (
    <Container>
      <h1>Results</h1>
      <pre>{JSON.stringify(state, null, 2)}</pre>
    </Container>
  )
}
