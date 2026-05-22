// ==============================================
// EDULEARN ADMIN CUSTOM JAVASCRIPT
// ==============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('EduLearn Admin Custom JS Loaded');
    
    // ===== YOUTUBE URL AUTO-EXTRACT =====
    const youtubeUrlField = document.getElementById('id_youtube_url');
    const youtubeIdField = document.getElementById('id_youtube_id');
    
    if (youtubeUrlField && youtubeIdField) {
        console.log('YouTube fields found');
        
        youtubeUrlField.addEventListener('blur', function() {
            const url = this.value.trim();
            console.log('YouTube URL entered:', url);
            
            if (url) {
                let videoId = '';
                
                // Extract YouTube ID from different URL formats
                if (url.includes('youtube.com/watch?v=')) {
                    videoId = url.split('v=')[1];
                    const ampersandPosition = videoId.indexOf('&');
                    if (ampersandPosition !== -1) {
                        videoId = videoId.substring(0, ampersandPosition);
                    }
                } else if (url.includes('youtu.be/')) {
                    videoId = url.split('youtu.be/')[1];
                    const questionMarkPosition = videoId.indexOf('?');
                    if (questionMarkPosition !== -1) {
                        videoId = videoId.substring(0, questionMarkPosition);
                    }
                } else if (url.includes('youtube.com/embed/')) {
                    videoId = url.split('embed/')[1];
                    const slashPosition = videoId.indexOf('/');
                    if (slashPosition !== -1) {
                        videoId = videoId.substring(0, slashPosition);
                    }
                }
                
                // Clean video ID
                videoId = videoId.replace(/[^a-zA-Z0-9_-]/g, '');
                
                if (videoId && videoId.length === 11) {
                    console.log('Extracted YouTube ID:', videoId);
                    youtubeIdField.value = videoId;
                    
                    // Show/hide preview
                    showYouTubePreview(videoId);
                } else {
                    console.log('Invalid YouTube URL format');
                    alert('Please enter a valid YouTube URL');
                }
            }
        });
        
        // Auto-extract on page load if URL exists
        if (youtubeUrlField.value) {
            youtubeUrlField.dispatchEvent(new Event('blur'));
        }
    }
    
    // ===== SLUG AUTO-GENERATION =====
    const titleFields = document.querySelectorAll('#id_title, #id_name');
    const slugFields = document.querySelectorAll('#id_slug');
    
    if (titleFields.length > 0 && slugFields.length > 0) {
        titleFields.forEach((titleField, index) => {
            if (slugFields[index]) {
                titleField.addEventListener('blur', function() {
                    if (!slugFields[index].value) {
                        const slug = generateSlug(this.value);
                        slugFields[index].value = slug;
                        console.log('Auto-generated slug:', slug);
                    }
                });
            }
        });
    }
    
    // ===== THUMBNAIL PREVIEW =====
    const thumbnailInput = document.querySelector('input[type="file"][name*="thumbnail"], input[type="file"][name*="logo"]');
    if (thumbnailInput) {
        thumbnailInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(e.target.result, file.name);
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // ===== FORM VALIDATION =====
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add your custom validation here
            console.log('Form submitted:', this.id || 'unknown form');
        });
    });
    
    // ===== HELPER FUNCTIONS =====
    
    function generateSlug(text) {
        return text
            .toLowerCase()
            .replace(/[^\w\s]/gi, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-')
            .substring(0, 50);
    }
    
    function showYouTubePreview(videoId) {
        // Remove existing preview
        const existingPreview = document.getElementById('youtube-admin-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // Create preview container
        const previewDiv = document.createElement('div');
        previewDiv.id = 'youtube-admin-preview';
        previewDiv.className = 'youtube-preview';
        
        // Preview content
        previewDiv.innerHTML = `
            <h4><i class="fab fa-youtube"></i> YouTube Preview</h4>
            <p><strong>Video ID:</strong> ${videoId}</p>
            <div class="thumbnail-container">
                <img src="https://img.youtube.com/vi/${videoId}/hqdefault.jpg" 
                     alt="YouTube Thumbnail Preview"
                     class="admin-thumbnail">
                <p class="small">Standard Quality Thumbnail (480×360)</p>
            </div>
            <div class="mt-2">
                <a href="https://youtube.com/watch?v=${videoId}" 
                   target="_blank" 
                   class="button" 
                   style="background: #ff0000; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">
                    <i class="fab fa-youtube"></i> Test Link
                </a>
                <button type="button" 
                        onclick="navigator.clipboard.writeText('${videoId}')"
                        class="button"
                        style="background: #6c757d; color: white; padding: 5px 10px; border-radius: 3px; border: none; margin-left: 10px;">
                    <i class="fas fa-copy"></i> Copy ID
                </button>
            </div>
        `;
        
        // Insert after YouTube URL field
        if (youtubeUrlField && youtubeUrlField.parentNode) {
            youtubeUrlField.parentNode.appendChild(previewDiv);
        }
    }
    
    function showImagePreview(imageData, fileName) {
        // Remove existing preview
        const existingPreview = document.getElementById('image-admin-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // Create preview container
        const previewDiv = document.createElement('div');
        previewDiv.id = 'image-admin-preview';
        previewDiv.className = 'youtube-preview';
        previewDiv.style.borderLeftColor = '#28a745';
        
        // Preview content
        previewDiv.innerHTML = `
            <h4><i class="fas fa-image"></i> Image Preview</h4>
            <p><strong>File:</strong> ${fileName}</p>
            <div class="thumbnail-container">
                <img src="${imageData}" 
                     alt="Image Preview"
                     class="admin-thumbnail"
                     style="max-height: 150px;">
            </div>
        `;
        
        // Insert after file input
        const fileInputs = document.querySelectorAll('input[type="file"]');
        if (fileInputs.length > 0) {
            fileInputs[fileInputs.length - 1].parentNode.appendChild(previewDiv);
        }
    }
    
    // ===== DURATION FORMAT HELPER =====
    const durationField = document.getElementById('id_duration');
    if (durationField) {
        durationField.placeholder = 'HH:MM:SS or MM:SS';
        
        durationField.addEventListener('blur', function() {
            let duration = this.value.trim();
            
            // Convert simple numbers to time format
            if (/^\d+$/.test(duration)) {
                const minutes = parseInt(duration);
                if (minutes < 60) {
                    this.value = `00:${minutes.toString().padStart(2, '0')}:00`;
                } else {
                    const hours = Math.floor(minutes / 60);
                    const mins = minutes % 60;
                    this.value = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:00`;
                }
            }
            // Ensure proper format
            else if (duration && !/^\d{2}:\d{2}:\d{2}$/.test(duration)) {
                const parts = duration.split(':');
                if (parts.length === 2) {
                    // MM:SS -> HH:MM:SS
                    this.value = `00:${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`;
                }
            }
        });
    }
    
    // ===== AUTO-SAVE REMINDER =====
    let formChanged = false;
    const formInputs = document.querySelectorAll('form input, form textarea, form select');
    
    formInputs.forEach(input => {
        input.addEventListener('change', function() {
            formChanged = true;
        });
    });
    
    window.addEventListener('beforeunload', function(e) {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
        }
    });
});