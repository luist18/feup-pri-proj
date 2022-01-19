import React, { ReactElement } from 'react'

import moment from 'moment'
import 'moment/locale/pt'
import { QueryDocument } from 'types/solr'
import { capitalize } from 'util/word'

import { Container } from './style'

interface Props {
  document: QueryDocument
}

function stateColor(state: string | undefined): string {
  switch (state) {
    case 'consolidado':
      return 'var(--article-state-green)'
    case 'alterado':
      return 'var(--article-state-yellow)'
    case 'revogado':
      return 'var(--article-state-red)'
    default:
      return 'var(--article-path)'
  }
}

export default function ArticleCard({ document }: Props): ReactElement {
  return (
    <Container className="flex flex-col">
      <header className="flex items-center mb-2">
        <h2 className="text-xl font-semibold article-title">{`Artigo ${document.key}º (${document.title})`}</h2>
        <span
          className="ml-auto h-full text-sm font-medium text-white py-1.5 px-3 rounded-xl"
          style={{
            backgroundColor: stateColor(document.state?.toLowerCase()),
          }}
        >
          {capitalize(document.state || 'Sem estado')}
        </span>
      </header>
      <main className="mb-2">
        <p className="article-text">
          {document.text.replaceAll('\\n', '\n').trim()}
        </p>
      </main>
      <footer className="flex flex-col">
        <span className="article-path text-sm">
          {[
            document.book,
            ...document.path.map((element) => capitalize(element)),
          ].join(' > ')}
        </span>
        <span className="article-date ml-auto my-2">
          {moment(new Date(document.date))
            .locale('PT')
            .format('D [de] MMMM [de] YYYY')}
        </span>
      </footer>
    </Container>
  )
}
