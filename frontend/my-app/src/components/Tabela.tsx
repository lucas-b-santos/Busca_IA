import React from 'react';
import { InfoBusca } from '@/definitions';

const ResultadoTabela = ({ result } : { result : InfoBusca}) => {
  return (
    <div className='w-100'>
      <h2>Resultados</h2>

      {/* Tabela para Hill Climbing */}
      <table border={1} cellPadding="10" cellSpacing="0" className='w-100'>
        <caption><strong>Hill Climbing</strong></caption>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Nós Gerados</td>
            <td>{result.nos_gerados_hill}</td>
          </tr>
          <tr>
            <td>Nós Visitados</td>
            <td>{result.nos_visitados_hill}</td>
          </tr>
          <tr>
            <td>Tempo de Execução (segundos)</td>
            <td>{result.tempo_exec_hill.toFixed(4)}</td>
          </tr>
          <tr>
            <td>Memória Usada (KB)</td>
            <td>{result.memoria_usada_hill.toFixed(4)}</td>
          </tr>
        </tbody>
      </table>

      <br />

      {/* Tabela para Busca em Largura */}
      <table border={1} cellPadding="10" cellSpacing="0" className='w-100'>
        <caption><strong>Busca em Largura</strong></caption>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Nós Gerados</td>
            <td>{result.nos_gerados_largura}</td>
          </tr>
          <tr>
            <td>Nós Visitados</td>
            <td>{result.nos_visitados_largura}</td>
          </tr>
          <tr>
            <td>Tempo de Execução (segundos)</td>
            <td>{result.tempo_exec_largura.toFixed(4)}</td>
          </tr>
          <tr>
            <td>Memória Usada (KB)</td>
            <td>{result.memoria_usada_largura.toFixed(4)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default ResultadoTabela;
