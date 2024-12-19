import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';
import Puzzle from '@/components/Puzzle';

export default function Home() {
  return (
    <>
      <Container className="mt-4 text-center">
        <h2>Comparação de Algoritmos de Busca </h2>
        <h3>Busca em Largura e Subindo a Montanha</h3>
        <Puzzle/>
      </Container>
    </>
  );
}
