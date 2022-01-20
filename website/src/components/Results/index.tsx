import React, { ReactElement } from 'react'

import ArticleCard from 'components/ArticleCard'
import ResultsPagination from 'components/ResultsPagination'
import { useSearch } from 'context/search'
import { numberWithSpaces } from 'util/word'

import { Container } from './style'

export default function Results(): ReactElement {
  const { searchQuery, search, state } = useSearch()

  const cards = state.results.map((document) => (
    <ArticleCard key={document.id} document={document} />
  ))

  if (state.loading) {
    return (
      <Container className="flex flex-col mt-8">
        <header className="my-4">
          <span className="text-lg app-grey font-medium">A procurar...</span>
        </header>
      </Container>
    )
  }

  return (
    <Container className="flex flex-col mt-8">
      <header className="my-4">
        <span className="text-lg app-grey font-medium">
          {numberWithSpaces(state.count)}{' '}
          {state.count === 1
            ? 'resultado encontrado'
            : 'resultados encontrados'}
        </span>
      </header>
      <main className="space-y-5">{cards}</main>
      <footer>
        {state.count > 0 ? (
          <ResultsPagination
            count={state.count}
            length={state.results.length}
            start={state.start}
            onPrevious={() => {
              searchQuery(search, state.page - 1)
            }}
            onNext={() => {
              searchQuery(search, state.page + 1)
            }}
          />
        ) : undefined}
      </footer>
    </Container>
  )
}
