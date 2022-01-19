import styled from 'styled-components'

export const Container = styled.div`
  background-color: var(--article-background);

  border-radius: var(--article-border-radius);
  box-shadow: var(--article-box-shadow);

  padding: 1.5rem;

  cursor: pointer;

  transition: transform 0.2s ease-in-out;

  :hover {
    transform: scale(1.005);
  }

  .article-title {
    color: var(--article-title);
  }

  .article-text {
    color: var(--article-text);
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .article-path,
  .article-date {
    color: var(--article-path);
  }
`
