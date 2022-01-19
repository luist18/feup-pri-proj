import React, { ReactElement } from 'react'

import ArticleCard from 'components/ArticleCard'
import { useSearch } from 'context/search'
import { numberWithSpaces } from 'util/word'

import { Container } from './style'

export default function Results(): ReactElement {
  const { state } = useSearch()

  const cards = state.results.map((document) => (
    <ArticleCard key={document.id} document={document} />
  ))

  return (
    <Container className="flex flex-col">
      <span className="my-4 text-lg app-grey font-medium">
        {numberWithSpaces(state.count)} resultados encontrados
      </span>
      <main className="space-y-5">{cards}</main>
    </Container>
  )
}
