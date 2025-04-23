
function openModal(idModal) {
    document.querySelector(`#${idModal}`).classList.add("show");
}

function closeModal(idModal) {
    // Se for o modal de auditoria, verifica os botões de salvar
    if (idModal === "auditoriaRecordModal") {
        // Seleciona os botões de auditoria (conformidade e followup)
        var unsavedButtons = $("#edit-auditoria-conformidade, #edit-auditoria-followup").filter(function() {
            return !$(this).hasClass("btn-locked");
        });
        
        // Se existir pelo menos um botão sem a classe btn-locked, não fecha o modal
        if (unsavedButtons.length > 0) {
            $("#warningModal").addClass("show");
            return;
        }
    }
    
    // Se não houver pendências ou se for outro modal, fecha normalmente
    document.querySelector(`#${idModal}`).classList.remove("show");
}


function showMessage(type, message) {
    // Define o ID da mensagem com base no tipo (success ou error)
    const messageId = type === 'success' ? 'success-message' : 'error-message';
    const textId = type === 'success' ? 'message-success-text' : 'message-error-text';

    // Obtém os elementos
    const messageContainer = document.getElementById(messageId);
    const messageText = document.getElementById(textId);

    if (messageContainer && messageText) {
        // Altera o texto da mensagem
        messageText.textContent = message;

        // Remove a classe display-none para exibir a mensagem
        messageContainer.classList.remove('display-none');

        // Fecha automaticamente após 5 segundos
        setTimeout(() => {
            closeMessages(messageId);
        }, 5000);
    }
}

function closeMessages(idModal) {
    document.querySelector(`#${idModal}`).classList.add("display-none");
}


// Função que salva os dados de acordo com a categoria (conformidade ou followup)
function saveData(category) {
    // Seleciona o container e os níveis de acordo com a categoria
    var containerId = (category === 'conformidade') ? '#auditoria_conformidade_container' : '#auditoria_followup_container';
    var level1Id = (category === 'conformidade') ? '#level_1_container_conformidade' : '#level_1_container_followup';
    var level2Id = (category === 'conformidade') ? '#level_2_container_conformidade' : '#level_2_container_followup';

    // Recupera o id da auditoria
    var auditId = $(containerId).attr("auditoria-id");

    // Objeto para armazenar os dados de cada nível
    var dataToSave = {
        level1: [],
        level2: []
    };

    // Itera pelos itens do Level 1 (pattern 1)
    $(containerId).find(level1Id).find(".item-audit").each(function () {
        var option = $(this).find("input[data-pattern='1'][data-category='" + category + "']").val();
        var constatacao = $(this).find("textarea[data-pattern='1'][data-category='" + category + "']").val();
        dataToSave.level1.push({
            option: option || null,
            constatacao: constatacao || ""
        });
    });

    // Itera pelos itens do Level 2 (pattern 2)
    $(containerId).find(level2Id).find(".item-audit").each(function () {
        var option = $(this).find("input[data-pattern='2'][data-category='" + category + "']").val();
        var constatacao = $(this).find("textarea[data-pattern='2'][data-category='" + category + "']").val();
        dataToSave.level2.push({
            option: option || null,
            constatacao: constatacao || ""
        });
    });

    // Armazena os dados no localStorage utilizando o id da auditoria
    localStorage.setItem('auditoria_' + category + '_' + auditId, JSON.stringify(dataToSave));
}

// Função para carregar os dados salvos para uma determinada categoria
function loadData(category) {
    // Seleciona o container e os níveis de acordo com a categoria
    var containerId = (category === 'conformidade') ? '#auditoria_conformidade_container' : '#auditoria_followup_container';
    var level1Id = (category === 'conformidade') ? '#level_1_container_conformidade' : '#level_1_container_followup';
    var level2Id = (category === 'conformidade') ? '#level_2_container_conformidade' : '#level_2_container_followup';

    // Recupera o id da auditoria
    var auditId = $(containerId).attr("auditoria-id");
    var storedData = localStorage.getItem('auditoria_' + category + '_' + auditId);

    if (storedData) {
        var data = JSON.parse(storedData);

        // Recupera os dados do Level 1 (pattern 1)
        $(containerId).find(level1Id).find(".item-audit").each(function (index) {
            if (data.level1[index]) {
                var savedOption = data.level1[index].option;
                var savedConstatacao = data.level1[index].constatacao;
                var inputField = $(this).find("input[data-pattern='1'][data-category='" + category + "']");

                // Preenche o input com a opção salva
                inputField.val(savedOption);

                // Marca a opção selecionada adicionando a classe "unique-option-active"
                $(this).find(".option-audit-select").each(function () {
                    if ($(this).text() === savedOption) {
                        $(this).addClass("unique-option-active");
                    } else {
                        $(this).removeClass("unique-option-active");
                    }
                });

                // Preenche a constatação
                $(this).find("textarea[data-pattern='1'][data-category='" + category + "']").val(savedConstatacao);
            }
        });

        // Recupera os dados do Level 2 (pattern 2)
        $(containerId).find(level2Id).find(".item-audit").each(function (index) {
            if (data.level2[index]) {
                var savedOption = data.level2[index].option;
                var savedConstatacao = data.level2[index].constatacao;
                var inputField = $(this).find("input[data-pattern='2'][data-category='" + category + "']");

                // Preenche o input com a opção salva
                inputField.val(savedOption);

                // Marca a opção selecionada
                $(this).find(".option-audit-select").each(function () {
                    if ($(this).text() === savedOption) {
                        $(this).addClass("unique-option-active");
                    } else {
                        $(this).removeClass("unique-option-active");
                    }
                });

                // Preenche a constatação
                $(this).find("textarea[data-pattern='2'][data-category='" + category + "']").val(savedConstatacao);
            }
        });
        console.log('Dados carregados para auditoria_' + category + '_' + auditId, data);
    }
}

// Função para verificar se todos os itens obrigatórios foram preenchidos
// (tanto a opção escolhida quanto o campo de constatações).
function verificarObrigatorios(typeAudit) {
    let todosPreenchidos = true;
    // Seleciona o container de acordo com o tipo de auditoria
    let container = (typeAudit === 'conformidade') ?
        "#auditoria_conformidade_container" : "#auditoria_followup_container";

    // Itera apenas sobre os itens do container específico
    $(container).find(".item-audit").each(function () {
        // Verifica se o item tem o asterisco (obrigatório)
        const temAsterisco = $(this).find("span[style*='color: red']").length > 0;
        if (temAsterisco) {
            // Obtém o valor do input hidden e do textarea
            const valorHidden = $(this).find("input[type='text']").val().trim();
            const valorTextarea = $(this).find("textarea").val().trim();

            // Se faltar a opção ou o texto da constatação, marca como incompleto
            if (!valorHidden || !valorTextarea) {
                todosPreenchidos = false;
                return false; // sai do loop
            }
        }
    });

    // Atualiza o estado do botão de acordo com o tipo de auditoria
    if (typeAudit === 'conformidade') {
        if (todosPreenchidos) {
            $("#finish-auditoria-conformidade").removeClass("btn-locked");
        } else {
            $("#finish-auditoria-conformidade").addClass("btn-locked");
        }
    } else if (typeAudit === 'followup') {
        if (todosPreenchidos) {
            $("#finish-auditoria-followup").removeClass("btn-locked");
        } else {
            $("#finish-auditoria-followup").addClass("btn-locked");
        }
    }
}

function verificarAlteracoes(typeAudit) {
    let houveAlteracao = false;

    // Seleciona o container de acordo com o tipo de auditoria
    let container = (typeAudit === 'conformidade') ?
        "#auditoria_conformidade_container" : "#auditoria_followup_container";

    // Itera sobre cada item da auditoria followup
    $(container).find(".item-audit").each(function () {
        // Obtém os valores originais dos atributos data
        const originalOption = $(this).data('original-option') ? $(this).data('original-option').toString().trim() : "";
        const originalConstatacao = $(this).data('original-constatacao') ? $(this).data('original-constatacao').toString().trim() : "";

        // Obtém os valores atuais do input e do textarea
        const atualOption = $(this).find("input[type='text']").val().trim();
        const atualConstatacao = $(this).find("textarea").val().trim();

        // Se os valores atuais forem diferentes dos originais, houve modificação
        if (originalOption.toLowerCase() !== atualOption.toLowerCase() || originalConstatacao !== atualConstatacao) {
            houveAlteracao = true;
            return false; // sai do loop assim que detectar uma alteração
        }
    });

    // Atualiza o estado do botão de finalizar auditoria followup
    if (houveAlteracao) {
        // Atualiza o estado do botão de acordo com o tipo de auditoria
        if (typeAudit === 'conformidade') {
            $("#edit-auditoria-conformidade").removeClass("btn-locked");
        } else if (typeAudit === 'followup') {
            $("#edit-auditoria-followup").removeClass("btn-locked");
        }
    } else {
        if (typeAudit === 'conformidade') {
            $("#edit-auditoria-conformidade").addClass("btn-locked");
        } else if (typeAudit === 'followup') {
            $("#edit-auditoria-followup").addClass("btn-locked");
        }
    }
}

function requestAjax(endpoint, payload) {
    // Envia o AJAX com o payload
    $.ajax({
        url: `http://127.0.0.1:8000/auditoria/api/v1/${endpoint}/`,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(payload),
        success: function (response) {
            console.log(response.redirect_url)
            window.location.href = response.redirect_url;

            if (endpoint == 'send') {
                localStorage.removeItem(`auditoria_${auditType}_${auditoriaId}`);
            }

        },
        error: function (error) {
            alert("Erro ao enviar auditoria.");
            console.error(error);
        }
    });
}

function getPayloadAction(auditType, typeAction) {
    // Define os seletores e o tipo de auditoria com base no auditType
    let containerId, level1Container, level2Container, type_audit;
    if (auditType === 'conformidade') {
        containerId = "#auditoria_conformidade_container";
        level1Container = "#level_1_container_conformidade";
        level2Container = "#level_2_container_conformidade";
        type_audit = "auditoria_de_conformidade";
    } else if (auditType === 'followup') {
        containerId = "#auditoria_followup_container";
        level1Container = "#level_1_container_followup";
        level2Container = "#level_2_container_followup";
        type_audit = "auditoria_de_followup";
    } else {
        console.error("Tipo de auditoria inválido");
        return;
    }

    // Verifica se o botão está bloqueado
    if ($(containerId).find(".btn-locked").length > 0) {
        showMessage('error', 'Ainda existem campos obrigatórios a serem preenchidos');
        return;
    }

    let listAudit1 = [];
    let listAudit2 = [];

    // Itera sobre os itens do container do nível 1
    $(level1Container + " .item-audit").each(function () {
        let uniqueOptionActive = $(this).find(".unique-option-active");
        if (uniqueOptionActive.length > 0) {
            let level = $(this).find(".unique-option-audit").attr("id").split("_")[1]; // Pega o número do nível
            let valueOption = uniqueOptionActive.attr("id").split("_")[1]; // Opção selecionada
            let constatacao = $(this).find("textarea").val(); // Texto da constatação

            listAudit1.push({
                level: parseInt(level),
                value_option: valueOption,
                constatacao: constatacao
            });
        }
    });

    // Itera sobre os itens do container do nível 2
    $(level2Container + " .item-audit").each(function () {
        let uniqueOptionActive = $(this).find(".unique-option-active");
        if (uniqueOptionActive.length > 0) {
            let level = $(this).find(".unique-option-audit").attr("id").split("_")[1];
            let valueOption = uniqueOptionActive.attr("id").split("_")[1];
            let constatacao = $(this).find("textarea").val();

            listAudit2.push({
                level: parseInt(level),
                value_option: valueOption,
                constatacao: constatacao
            });
        }
    });

    // Obtém o id da auditoria a partir do container principal
    const auditoriaId = $(containerId).attr("auditoria-id");

    // Monta os objetos para cada padrão
    let pattern1Json = {
        id_audit: parseInt(auditoriaId),
        type_audit: type_audit,
        pattern: 1,
        list_audit: listAudit1
    };

    let pattern2Json = {
        id_audit: parseInt(auditoriaId),
        type_audit: type_audit,
        pattern: 2,
        list_audit: listAudit2
    };

    let payload = {
        pattern_1: pattern1Json,
        pattern_2: pattern2Json
    };

    if (typeAction == 'Finish') {
        requestAjax('send', payload);
    } else if (typeAction == 'Edit') {
        requestAjax('edit', payload)
    }
}


function createBarChart(chartId, labels, dataValues, labelText) {
    const ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: labelText,
                data: dataValues,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }
    });
}


