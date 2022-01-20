import styled from 'styled-components'

export const Container = styled.div`
  input {
    color: var(--article-text);

    transition: outline 0.1s ease-out;
  }

  input::placeholder {
    color: var(--article-path);
  }

  input:focus {
    outline: solid 4px rgba(25, 50, 75, 0.3);
  }
`
