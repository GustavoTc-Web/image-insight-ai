(() => {
    'use strict';

    const form = document.getElementById('upload-form');
    const input = document.getElementById('image-input');
    const zone = document.getElementById('drop-zone');
    const selection = document.getElementById('selected-file');
    const preview = document.getElementById('image-preview');
    const filename = document.getElementById('file-name');
    const filesize = document.getElementById('file-size');
    const remove = document.getElementById('remove-image');
    const selectLabel = document.getElementById('select-label');
    const submit = document.getElementById('analyze-button');
    const submitLabel = document.getElementById('analyze-label');
    const error = document.getElementById('upload-error');
    const status = document.getElementById('upload-status');
    const maxSize = 8 * 1024 * 1024;
    let previewUrl = null;
    let dragging = 0;
    let submitting = false;

    function clearPreview() {
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        previewUrl = null;
        preview.hidden = true;
        preview.removeAttribute('src');
    }

    function showError(message) {
        error.textContent = message;
        error.hidden = !message;
    }

    function updateSelection() {
        clearPreview();
        showError('');
        const file = input.files[0];
        let message = '';
        if (file && !/\.(png|jpe?g|webp)$/i.test(file.name)) {
            message = 'Selecione uma imagem PNG, JPG, JPEG ou WEBP.';
        } else if (file && file.size === 0) {
            message = 'O arquivo está vazio. Selecione outra imagem.';
        } else if (file && file.size > maxSize) {
            message = 'A imagem ultrapassa 8 MB. Selecione um arquivo menor.';
        }
        if (message) input.value = '';
        const valid = Boolean(file && !message);
        selection.hidden = !valid;
        submit.disabled = !valid;
        selectLabel.textContent = valid ? 'Trocar imagem' : 'Selecionar imagem';
        filename.textContent = valid ? file.name : '';
        filesize.textContent = valid ? (file.size / 1024 / 1024 >= 1
            ? `${(file.size / 1024 / 1024).toFixed(2)} MB`
            : `${(file.size / 1024).toFixed(1)} KB`) : '';
        status.textContent = valid ? `Imagem selecionada: ${file.name}. Pronta para análise.` : 'Nenhuma imagem selecionada.';
        if (valid) {
            previewUrl = URL.createObjectURL(file);
            preview.src = previewUrl;
            preview.hidden = false;
        }
        showError(message);
    }

    input.addEventListener('change', updateSelection);
    // A failed preview must not prevent the existing backend from receiving the file.
    preview.addEventListener('error', () => { preview.hidden = true; });
    remove.addEventListener('click', () => {
        input.value = '';
        updateSelection();
        input.focus();
    });

    zone.addEventListener('dragenter', (event) => {
        event.preventDefault();
        if (!submitting) {
            dragging += 1;
            zone.classList.add('is-dragging');
        }
    });
    zone.addEventListener('dragover', (event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = submitting ? 'none' : 'copy';
    });
    zone.addEventListener('dragleave', () => {
        dragging = Math.max(0, dragging - 1);
        if (!dragging) zone.classList.remove('is-dragging');
    });
    zone.addEventListener('drop', (event) => {
        event.preventDefault();
        dragging = 0;
        zone.classList.remove('is-dragging');
        if (submitting) return;
        const files = event.dataTransfer.files;
        if (files.length !== 1) {
            showError('Selecione uma única imagem por análise.');
            return;
        }
        // Assign to the real input so the native multipart POST includes the file.
        try {
            input.files = files;
        } catch {
            showError('Use o botão Selecionar imagem para escolher o arquivo.');
            return;
        }
        updateSelection();
    });

    form.addEventListener('submit', (event) => {
        if (submitting || !input.files.length || submit.disabled) {
            event.preventDefault();
            return;
        }
        submitting = true;
        submit.disabled = true;
        remove.disabled = true;
        // Keep the file input enabled: disabled inputs are omitted from the POST.
        submitLabel.textContent = 'Analisando imagem…';
        status.textContent = 'Análise em andamento. Aguarde o resultado.';
        form.setAttribute('aria-busy', 'true');
    });
    input.addEventListener('click', (event) => {
        if (submitting) event.preventDefault();
    });
    window.addEventListener('pageshow', () => {
        submitting = false;
        remove.disabled = false;
        submitLabel.textContent = 'Analisar imagem';
        form.removeAttribute('aria-busy');
        updateSelection();
    });
    updateSelection();
})();
