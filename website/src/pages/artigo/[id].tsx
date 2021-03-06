import { GetServerSidePropsContext } from 'next'
import Head from 'next/head'

import React from 'react'

import Article from 'components/Article'
import Footer from 'components/Footer'
import Header from 'components/Header'
import Layout from 'components/Layout'
import { fetchArticle } from 'service/articles'
import { QueryDocument } from 'types/solr'

type Props = {
  document: QueryDocument | undefined
  related: QueryDocument[]
}

export const getServerSideProps = async ({
  query,
}: GetServerSidePropsContext) => {
  const { id } = query

  if (id === undefined) {
    return {
      props: {
        related: [],
      },
    }
  }

  const request = await fetchArticle(id?.toString())

  return {
    props: {
      document: request.article || null,
      related: request.related,
    },
  }
}

function Results({ document, related }: Props): React.ReactElement {
  return (
    <>
      <Head>
        <title>Resultados | Legislação Portuguesa</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header />
      <Layout>
        <Article document={document} related={related} />
      </Layout>
      <Footer />
    </>
  )
}

export default Results
