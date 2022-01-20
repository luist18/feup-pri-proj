import styled from 'styled-components'

export const Container = styled.div`
  grid-area: content;

  max-width: 930px;

  .article-title {
    color: var(--article-title);
  }

  .article-text {
    color: var(--article-text);
  }

  .article-path,
  .article-date {
    color: var(--article-path);
  }
`
