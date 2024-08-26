// static/js/scripts.js

//CROPPER IMAGES FUNCTIONS
function showCropper(event) {
    const files = event.target.files;
    const imgContainer = document.querySelector('.img-container');

    if (files && files.length > 0) {
        const file = files[0];
        const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!validImageTypes.includes(file.type)) {
            alert('Por favor, selecione uma imagem válida (JPEG, PNG, GIF).');
            event.target.value = ''; // Limpa o input
            imgContainer.style.display = 'none'; // Esconde a área de visualização da imagem
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            image.src = e.target.result;
            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(image, {
                aspectRatio: NaN, // Liberdade para escolher a proporção
                viewMode: 1,
            });
            imgContainer.style.display = 'block'; // Mostra a área de visualização da imagem
        };
        reader.readAsDataURL(file);
    } else {
        imgContainer.style.display = 'none'; // Esconde a área de visualização da imagem
    }
}

function submitForm(event) {
    event.preventDefault();
    const form = event.target;
    document.getElementById('loading-spinner').style.display = 'block';

    const formData = new FormData(form);

    if (cropper && document.getElementById('image').files.length > 0) {
        cropper.getCroppedCanvas().toBlob((blob) => {
            const fileName = 'cropped_image.png';
            const croppedImage = new File([blob], fileName, { type: 'image/png' });
            formData.append('image', croppedImage);
            sendFormData(form.action, formData);
        }, 'image/png');
    } else {
        sendFormData(form.action, formData);
    }
}

// Outras funções comuns aqui
