function uniqueOptionConfig(arrowId, inputId, popupId, itemClass, divClickContainer, hiddenInputId) {

    $(document).on('click', arrowId, function () {
        const searchInput = $(inputId);
        searchInput.attr('placeholder', 'Digite para pesquisar');
        $(popupId).toggle();
        searchInput.focus();
    });

    $(document).on('click', itemClass, function () { // Delegação para itens dinâmicos
        const selectedOption = $(this).find('.flow-hnsd-p').text().trim();
        const selectedId = $(this).attr('data-id'); // Obtém o ID do atributo data-id

        // Define o valor do input visível
        $(inputId).val(selectedOption);

        // Define o valor do input hidden para o ID selecionado
        $(hiddenInputId).val(parseInt(selectedId));

        // Esconde o popup
        $(popupId).hide();
    });

    $(document).on('click', function (event) {
        if (!$(event.target).closest(divClickContainer).length) { // Fora do container
            $(popupId).hide();
        }
    });

    $(document).on('input', inputId, function () {
        const filter = $(this).val().toLowerCase();
        let visibleCount = 0;
        $(itemClass).each(function () {
            const text = $(this).text().toLowerCase();
            if (text.includes(filter)) {
                $(this).show();
                visibleCount++;
            } else {
                $(this).hide();
            }
        });

        const container = $(popupId);
        if (visibleCount === 0) {
            if (!$('.no-results').length) {
                container.append('<div class="no-results flex-start"><span class="flow-hnsd-p">Nenhum resultado para "' + filter + '" encontrado</span></div>');
            }
        } else {
            $('.no-results').remove();
        }

        const optionHeight = 30; // Altura de cada item
        const maxHeight = optionHeight * visibleCount;
        container.css('height', maxHeight > 0 ? maxHeight : 'auto');
    });
}


function multiOptionConfig(arrowId, inputId, popupId, itemClass, divClickContainer, hiddenInputId) {
    $(document).on('click', arrowId, function () {
        const searchInput = $(inputId);
        searchInput.attr('placeholder', 'Digite para pesquisar');
        $(popupId).toggle();
        searchInput.focus();
    });

    $(document).on('click', function (event) {
        if (!$(event.target).closest(divClickContainer).length) {
            $(popupId).hide();
        }
    });

    $(document).on('input', inputId, function () {
        const filter = $(this).val().toLowerCase();
        let visibleCount = 0;
        $(itemClass).each(function () {
            const text = $(this).text().toLowerCase();
            if (text.includes(filter) || $(this).find('input[type="checkbox"]').attr('id') === 'all_select') {
                $(this).show();
                visibleCount++;
            } else {
                $(this).hide();
            }
        });

        const container = $(popupId);
        if (visibleCount === 0) {
            if (!$('.no-results').length) {
                container.append('<div class="no-results flex-start"><span class="flow-hnsd-p">Nenhum resultado para "' + filter + '" encontrado</span></div>');
            }
        } else {
            $('.no-results').remove();
        }

        const optionHeight = 30;
        const maxHeight = optionHeight * visibleCount;
        container.css('height', maxHeight > 0 ? maxHeight : 'auto');
    });

    // Checkbox geral: "Selecionar todos"
    $(document).on('change', '#all_select', function () {
        const checked = $(this).is(':checked');
        $(itemClass + ' input[type="checkbox"]').not('#all_select').prop('checked', checked).trigger('change');
    });

    // Atualiza hidden input com os setores selecionados
    $(document).on('change', itemClass + ' input[type="checkbox"]', function () {
        if ($(this).attr('id') === 'all_select') return;

        let selectedIds = [];
        $(itemClass + ' input[type="checkbox"]:checked').each(function () {
            const id = $(this).closest(itemClass).attr('data-id');
            if (id) selectedIds.push(id);
        });

        $(hiddenInputId).val(selectedIds.join(','));

        // Atualiza o "Selecionar todos" se necessário
        const total = $(itemClass + ' input[type="checkbox"]').not('#all_select').length;
        const checkedCount = $(itemClass + ' input[type="checkbox"]:checked').not('#all_select').length;
        $('#all_select').prop('checked', total > 0 && total === checkedCount);
    });
}
