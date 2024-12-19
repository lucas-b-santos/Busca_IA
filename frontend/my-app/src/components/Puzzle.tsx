import React, { useState } from "react";
import { Button, Container } from "react-bootstrap";
import { InfoBusca } from "@/definitions";
import ResultadoTabela from "./Tabela";
import { GridLoader } from "react-spinners";

const Puzzle = () => {
    const emptyMatrix = [["", "", ""],
    ["", "", ""],
    ["", "", ""]];

    // Estado para armazenar a matriz
    const [matrix, setMatrix] = useState(emptyMatrix);


    const [loading, setLoading] = useState(false); // Para controlar o estado de carregamento
    const [hasError, setHasError] = useState(false); // Para armazenar possíveis erros
    const [abortController, setAbortController] = useState<null | AbortController>(null);
    const [result, setResult] = useState<null | InfoBusca>(null);

    const toMatrix = (str: string) => {
        // Divida a string em um array de caracteres
        const chars = str.split('');

        // Transforme em uma matriz 3x3
        const matrix = [];

        for (let i = 0; i < 3; i++) {
            matrix.push(chars.slice(i * 3, (i + 1) * 3));
        }

        return matrix;
    }

    const isValueInMatrix = (matrix: string[][], value: string) => {
        return matrix.some((row) => row.includes(value));
    };

    // Atualiza o valor de uma célula específica
    const handleChange = (row: number, col: number, value: string) => {
        if (isValueInMatrix(matrix, value))
            return;

        if (value === "" || (value >= "0" && value <= "8")) {
            const newMatrix = [...matrix];
            newMatrix[row][col] = value;
            setMatrix(newMatrix);
        }
    };

    const handleGerarTabuleiro = () => {
        setHasError(false);
        fetch("http://127.0.0.1:5000/gerar_tabuleiro")
            .then((response) => response.json())
            .then((data) => {
                setMatrix(toMatrix(data.tabuleiro));
            })
            .catch((error) => {
                console.error("Error:", error)
                setHasError(true);
            });
    }

    const handleSubmit = async () => {
        setHasError(false);
        setResult(null);

        if (isValueInMatrix(matrix, "")) {
            setHasError(true);
            setMatrix(emptyMatrix);
            return;
        }

        const controller = new AbortController(); // Cria um novo AbortController
        setAbortController(controller); // Salva o controller no estado

        try {
            setLoading(true);

            const response = await fetch("http://127.0.0.1:5000/executar_algoritmos", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ tabuleiro: matrix.map(row => row.map(cell => parseInt(cell))) }), // Envia a matriz como JSON
                signal: controller.signal, // Passa o signal para a requisição
            });

            if (!response.ok) {
                setHasError(true);
                setMatrix(emptyMatrix);
            } else {
                const result = await response.json();
                console.log("Resposta do servidor:", result);
                setResult(result);
            }

        } catch (error) {
            console.error("Erro ao enviar o puzzle:", error);
        } finally {
            setLoading(false);
            setAbortController(null); // Reseta o controller ao final
        }

    };

    const cancelRequest = () => {
        if (abortController) {
            abortController.abort(); // Cancela a requisição
            setAbortController(null); // Reseta o controller
        }
    };

    const cleanTabuleiro = () => {
        setMatrix(emptyMatrix);
        setResult(null);
        setHasError(false);
    }

    return (
        <Container className="d-flex mt-5">
            <Container className="d-flex flex-column text-center">
                <h3>Tabuleiro</h3>
                <p style={{ marginTop: '10px', fontStyle: 'italic', color: 'gray' }}>
                    Gere os valores de forma aleatória ou insira no tabuleiro.
                </p>
                <table
                    style={{
                        margin: "0 auto",
                        borderCollapse: "collapse",
                    }}
                >
                    <tbody>
                        {matrix.map((row, rowIndex) => (
                            <tr key={rowIndex}>
                                {row.map((cell, colIndex) => (
                                    <td
                                        key={colIndex}
                                        style={{
                                            border: "1px solid #000",
                                            width: "50px",
                                            height: "50px",
                                        }}
                                    >
                                        <input
                                            type="text"
                                            maxLength={1} // Limita a um único caractere
                                            value={cell}
                                            onChange={(e) =>
                                                handleChange(rowIndex, colIndex, e.target.value)
                                            }
                                            style={{
                                                width: "100%",
                                                height: "100%",
                                                textAlign: "center",
                                                fontSize: "18px",
                                            }}
                                            disabled={loading} // Desabilita o campo enquanto carregando
                                        />
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>

                <p style={{ marginTop: '10px', fontStyle: 'italic', color: 'gray' }}>
                    Obs: casa vazia = 0
                </p>
                {hasError && <p className="text-danger">Tabuleiro inválido!</p>}
                <Container className="d-flex gap-3 justify-content-center">

                    <Button disabled={loading} variant="primary" onClick={handleGerarTabuleiro}>
                        Gerar Tabuleiro
                    </Button>

                    <Button disabled={loading} variant="success" onClick={handleSubmit}>
                        Executar Algoritmos
                    </Button>

                    <Button disabled={loading} variant="danger" onClick={cleanTabuleiro}>
                        Limpar
                    </Button>

                    <Button disabled={!loading} variant="danger" onClick={cancelRequest}>
                        Cancelar
                    </Button>
                </Container>

            </Container>
            <Container className="d-flex align-items-center justify-content-center">
                {result && <ResultadoTabela result={result} />}
                {loading && (
                    <Container>
                        <p>Executando algoritmos...</p>
                        <GridLoader></GridLoader>
                    </Container>)}
            </Container>
        </Container>

    );
};

export default Puzzle;
