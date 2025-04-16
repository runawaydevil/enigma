document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const processBtn = document.getElementById('process-btn');
    const addPairBtn = document.getElementById('add-pair');
    const plugboardInput = document.getElementById('plugboard-input');
    const plugboardPairs = document.getElementById('plugboard-pairs');
    const rotorSelects = [document.getElementById('rotor1'), document.getElementById('rotor2'), document.getElementById('rotor3')];
    const positionInputs = [document.getElementById('pos1'), document.getElementById('pos2'), document.getElementById('pos3')];

    let plugboardPairsList = [];

    // Função para processar o texto
    async function processText() {
        const text = inputText.value;
        const rotorPositions = positionInputs.map(input => {
            const value = input.value.toUpperCase();
            return value ? value.charCodeAt(0) - 'A'.charCodeAt(0) : 0;
        });

        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text,
                    rotorPositions,
                    plugboardPairs: plugboardPairsList
                })
            });

            const data = await response.json();
            outputText.value = data.result;
        } catch (error) {
            console.error('Erro ao processar texto:', error);
            alert('Erro ao processar texto. Por favor, tente novamente.');
        }
    }

    // Função para adicionar par ao plugboard
    function addPlugboardPair() {
        const pair = plugboardInput.value.toUpperCase();
        if (pair.length !== 2 || !/^[A-Z]{2}$/.test(pair)) {
            alert('Por favor, digite um par válido de letras (ex: AB)');
            return;
        }

        if (plugboardPairsList.some(p => p.includes(pair[0]) || p.includes(pair[1]))) {
            alert('Uma das letras já está em uso no plugboard');
            return;
        }

        plugboardPairsList.push(pair);
        updatePlugboardDisplay();
        plugboardInput.value = '';
    }

    // Função para atualizar a exibição do plugboard
    function updatePlugboardDisplay() {
        plugboardPairs.innerHTML = '';
        plugboardPairsList.forEach(pair => {
            const pairElement = document.createElement('div');
            pairElement.className = 'plugboard-pair';
            pairElement.textContent = pair;
            
            const removeBtn = document.createElement('button');
            removeBtn.className = 'btn btn-sm btn-danger';
            removeBtn.textContent = '×';
            removeBtn.onclick = () => {
                plugboardPairsList = plugboardPairsList.filter(p => p !== pair);
                updatePlugboardDisplay();
            };

            pairElement.appendChild(removeBtn);
            plugboardPairs.appendChild(pairElement);
        });
    }

    // Event listeners
    processBtn.addEventListener('click', processText);
    addPairBtn.addEventListener('click', addPlugboardPair);

    // Validação dos inputs de posição
    positionInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase().replace(/[^A-Z]/g, '');
        });
    });

    // Validação do input do plugboard
    plugboardInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.toUpperCase().replace(/[^A-Z]/g, '');
    });
}); 