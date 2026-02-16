// Modern Fruit Quality AI JavaScript
// Enhanced interactions and loading states

console.log("[SUCCESS] Fruit Quality AI initialized successfully!");

// Global variables
let isProcessing = false;
let currentFile = null;

// Utility functions
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const showLoading = (element, text = 'Processing...') => {
  if (!element) return;
  
  const originalContent = element.innerHTML;
  element.dataset.originalContent = originalContent;
  element.disabled = true;
  element.innerHTML = `
    <span class="spinner-border spinner-border-sm me-2" role="status">
      <span class="visually-hidden">Loading...</span>
    </span>
    ${text}
  `;
  element.classList.add('loading');
};

const hideLoading = (element) => {
  if (!element) return;
  
  const originalContent = element.dataset.originalContent;
  if (originalContent) {
    element.innerHTML = originalContent;
    element.disabled = false;
    element.classList.remove('loading');
    delete element.dataset.originalContent;
  }
};

const showToast = (message, type = 'info') => {
  const toastContainer = $('.toast-container') || createToastContainer();
  
  const toastId = 'toast-' + Date.now();
  const toastHTML = `
    <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0 animate__animated animate__fadeInRight" role="alert">
      <div class="d-flex">
        <div class="toast-body">
          <i class="fas fa-${getToastIcon(type)} me-2"></i>
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>
  `;
  
  toastContainer.insertAdjacentHTML('beforeend', toastHTML);
  
  const toastElement = $(`#${toastId}`);
  const toast = new bootstrap.Toast(toastElement, {
    autohide: true,
    delay: 5000
  });
  
  toast.show();
  
  toastElement.addEventListener('hidden.bs.toast', () => {
    toastElement.remove();
  });
};

const getToastIcon = (type) => {
  const icons = {
    'success': 'check-circle',
    'danger': 'exclamation-triangle',
    'warning': 'exclamation-circle',
    'info': 'info-circle'
  };
  return icons[type] || 'info-circle';
};

const createToastContainer = () => {
  const container = document.createElement('div');
  container.className = 'toast-container position-fixed top-0 end-0 p-3';
  container.style.zIndex = '9999';
  document.body.appendChild(container);
  return container;
};

// Form validation and submission
const form = $('#predictForm');
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (isProcessing) {
      showToast('Please wait for the current analysis to complete.', 'warning');
      return;
    }
    
    const fileInput = $('#image');
    const predictBtn = $('#predictBtn');
    
    if (!fileInput.files.length) {
      showToast('Please select an image before submitting!', 'warning');
      shakeElement(fileInput.closest('.drop-zone') || fileInput);
      return;
    }
    
    const file = fileInput.files[0];
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    
    if (!allowedTypes.includes(file.type)) {
      showToast('Invalid file type! Please upload a PNG or JPG image.', 'danger');
      shakeElement(fileInput.closest('.drop-zone') || fileInput);
      return;
    }
    
    if (file.size > 6 * 1024 * 1024) {
      showToast('File too large! Please upload under 6MB.', 'danger');
      shakeElement(fileInput.closest('.drop-zone') || fileInput);
      return;
    }
    
    // Show loading state
    isProcessing = true;
    showLoading(predictBtn, 'Analyzing...');
    
    // Add progress indicator
    const progressIndicator = createProgressIndicator();
    form.appendChild(progressIndicator);
    
    try {
      // Simulate progress (in real app, this would be actual upload progress)
      await simulateProgress(progressIndicator);
      
      // Submit form
      form.submit();
      
    } catch (error) {
      console.error('Submission error:', error);
      showToast('An error occurred during analysis. Please try again.', 'danger');
      hideLoading(predictBtn);
      isProcessing = false;
      progressIndicator.remove();
    }
  });
}

// Progress indicator
const createProgressIndicator = () => {
  const indicator = document.createElement('div');
  indicator.className = 'progress-indicator mt-3';
  indicator.innerHTML = `
    <div class="progress" style="height: 6px;">
      <div class="progress-bar progress-bar-striped progress-bar-animated" 
           role="progressbar" style="width: 0%" 
           aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
      </div>
    </div>
    <div class="progress-text text-center mt-2">
      <small class="text-muted">Initializing AI analysis...</small>
    </div>
  `;
  return indicator;
};

const simulateProgress = async (indicator) => {
  const progressBar = indicator.querySelector('.progress-bar');
  const progressText = indicator.querySelector('.progress-text small');
  
  const steps = [
    { progress: 20, text: 'Validating image format...' },
    { progress: 40, text: 'Preprocessing image...' },
    { progress: 60, text: 'Analyzing fruit type...' },
    { progress: 80, text: 'Assessing quality...' },
    { progress: 95, text: 'Finalizing results...' }
  ];
  
  for (const step of steps) {
    await new Promise(resolve => setTimeout(resolve, 500));
    progressBar.style.width = step.progress + '%';
    progressBar.setAttribute('aria-valuenow', step.progress);
    progressText.textContent = step.text;
  }
  
  // Keep at 95% until server response
  return new Promise(resolve => {
    setTimeout(resolve, 1000);
  });
};

// Shake animation for invalid elements
const shakeElement = (element) => {
  if (!element) return;
  
  element.classList.add('animate__animated', 'animate__shakeX');
  setTimeout(() => {
    element.classList.remove('animate__animated', 'animate__shakeX');
  }, 1000);
};

// Enhanced drag and drop
const dropZone = $('#dropZone');
if (dropZone) {
  // Prevent default drag behaviors
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });
  
  // Highlight drop zone when item is dragged over it
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.add('drag-over');
      dropZone.style.borderColor = '#667eea';
      dropZone.style.background = 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)';
    });
  });
  
  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.remove('drag-over');
      dropZone.style.borderColor = '#ddd';
      dropZone.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
    });
  });
  
  // Handle dropped files
  dropZone.addEventListener('drop', handleDrop);
}

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  
  if (files.length > 0) {
    const fileInput = $('#image');
    fileInput.files = files;
    handleFileSelect();
    
    // Visual feedback
    dropZone.classList.add('animate__animated', 'animate__bounceIn');
    setTimeout(() => {
      dropZone.classList.remove('animate__animated', 'animate__bounceIn');
    }, 1000);
  }
}

// File selection handler
function handleFileSelect() {
  const fileInput = $('#image');
  const file = fileInput.files[0];
  
  if (!file) return;
  
  currentFile = file;
  
  // Show file info
  const fileInfo = $('#fileInfo');
  const fileName = $('#fileName');
  const fileSize = $('#fileSize');
  const dropZone = $('#dropZone');
  const validationStatus = $('#validationStatus');
  
  if (fileInfo && fileName && fileSize) {
    fileName.textContent = file.name;
    fileSize.textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    fileInfo.classList.remove('d-none');
    
    if (dropZone) {
      dropZone.classList.add('d-none');
    }
  }
  
  // Validate file
  validateFile(file);
}

async function validateFile(file) {
  const predictBtn = $('#predictBtn');
  const validationStatus = $('#validationStatus');
  const fileInput = $('#image');
  
  // Show validation status
  if (validationStatus) {
    validationStatus.classList.remove('d-none');
    validationStatus.innerHTML = `
      <div class="d-flex align-items-center">
        <div class="spinner-border spinner-border-sm me-3" role="status">
          <span class="visually-hidden">Validating...</span>
        </div>
        <span class="text-muted">Validating image with AI...</span>
      </div>
    `;
  }
  
  // Disable predict button during validation
  if (predictBtn) {
    predictBtn.disabled = true;
  }
  
  try {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await fetch('/validate', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Validation failed');
    }
    
    const data = await response.json();
    
    // Hide validation status
    if (validationStatus) {
      validationStatus.classList.add('d-none');
    }
    
    if (data.valid === true) {
      // Valid image
      fileInput.classList.remove('is-invalid');
      if (predictBtn) {
        predictBtn.disabled = false;
        showToast('Image validated successfully! Ready for analysis.', 'success');
      }
    } else {
      // Invalid image - show inline display instead of modal
      const reason = data.label ? `${data.label} (${(data.confidence * 100).toFixed(2)}%)` : 'Low confidence';
      console.log('Invalid image detected, reason:', reason);
      fileInput.classList.add('is-invalid');
      if (predictBtn) {
        predictBtn.disabled = true;
      }
      
      // Call showInvalidImage with proper error handling
      try {
        showInvalidImage(file, reason);
      } catch (error) {
        console.error('Error in showInvalidImage:', error);
        showToast('Error displaying invalid image. Please try again.', 'danger');
      }
    }
    
  } catch (error) {
    console.error('Validation error:', error);
    
    // Hide validation status
    if (validationStatus) {
      validationStatus.classList.add('d-none');
    }
    
    // Re-enable predict button on error
    fileInput.classList.remove('is-invalid');
    if (predictBtn) {
      predictBtn.disabled = false;
    }
    
    showToast('Validation failed. You can still try submitting.', 'warning');
  }
}

// Clear file function
function clearFile() {
  const fileInput = $('#image');
  const fileInfo = $('#fileInfo');
  const dropZone = $('#dropZone');
  const validationStatus = $('#validationStatus');
  const predictBtn = $('#predictBtn');
  
  // Clear file input
  fileInput.value = '';
  currentFile = null;
  
  // Reset UI
  if (fileInfo) fileInfo.classList.add('d-none');
  if (dropZone) dropZone.classList.remove('d-none');
  if (validationStatus) validationStatus.classList.add('d-none');
  
  fileInput.classList.remove('is-invalid');
  if (predictBtn) predictBtn.disabled = false;
  
  // Add animation
  if (dropZone) {
    dropZone.classList.add('animate__animated', 'animate__fadeIn');
    setTimeout(() => {
      dropZone.classList.remove('animate__animated', 'animate__fadeIn');
    }, 1000);
  }
}

// Reset button handler
const resetBtn = $('#resetBtn');
if (resetBtn) {
  resetBtn.addEventListener('click', (e) => {
    e.preventDefault();
    clearFile();
    showToast('Form reset successfully', 'info');
  });
}

// Invalid image display function (replaces modal)
function showInvalidImage(file, reasonText) {
  console.log('showInvalidImage called with:', file, reasonText);
  
  const uploadSection = $('.upload-section');
  if (!uploadSection) {
    console.error('Upload section not found');
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    console.log('File loaded, creating invalid image section');
    
    const invalidImageHTML = `
      <div class="invalid-image-section animate__animated animate__fadeInUp">
        <div class="invalid-image-header">
          <div class="invalid-image-icon">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <h3 class="invalid-image-title">Invalid Fruit Image</h3>
          <p class="invalid-image-subtitle">We couldn't identify this as a supported fruit</p>
        </div>
        
        <div class="invalid-image-content">
          <div class="invalid-image-preview">
            <img src="${e.target.result}" alt="Invalid fruit image">
          </div>
          
          <div class="invalid-image-details">
            <h5>What went wrong?</h5>
            <p>${reasonText || 'Our AI couldn\'t confidently identify this as a fruit from our supported list. This could be due to poor image quality, lighting conditions, or the fruit may not be in our current database.'}</p>
            
            <div class="supported-fruits">
              <h6><i class="fas fa-check-circle me-2"></i>Supported Fruits</h6>
              <div class="fruit-tags">
                <span class="fruit-tag">🍎 Apple</span>
                <span class="fruit-tag">🍌 Banana</span>
                <span class="fruit-tag">🍋 Lemon</span>
                <span class="fruit-tag">🍊 Orange</span>
                <span class="fruit-tag">🥝 Guava</span>
                <span class="fruit-tag">🍋 Lime</span>
                <span class="fruit-tag">🍎 Pomegranate</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="invalid-image-actions">
          <button class="btn-retry" onclick="window.FruitAI.clearInvalidImage()">
            <i class="fas fa-redo me-2"></i>Try Another Image
          </button>
        </div>
      </div>
    `;
    
    // Insert the invalid image section after the upload card
    const uploadCard = $('.upload-card');
    if (uploadCard) {
      uploadCard.insertAdjacentHTML('afterend', invalidImageHTML);
      console.log('Invalid image section added');
    } else {
      console.error('Upload card not found');
    }
    
    // Hide the upload card
    if (uploadCard) {
      uploadCard.style.display = 'none';
    }
    
    // Scroll to the invalid image section
    setTimeout(() => {
      const invalidSection = $('.invalid-image-section');
      if (invalidSection) {
        invalidSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  };
  
  reader.onerror = function(error) {
    console.error('FileReader error:', error);
    showToast('Error reading image file', 'danger');
  };
  
  reader.readAsDataURL(file);
}

// Clear invalid image display
function clearInvalidImage() {
  console.log('clearInvalidImage called');
  
  const invalidSection = $('.invalid-image-section');
  const uploadCard = $('.upload-card');
  
  if (invalidSection) {
    invalidSection.remove();
    console.log('Invalid image section removed');
  }
  
  if (uploadCard) {
    uploadCard.style.display = 'block';
    console.log('Upload card shown');
  }
  
  clearFile();
  showToast('Ready to try with a new image!', 'info');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Ctrl/Cmd + O to open file dialog
  if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
    e.preventDefault();
    const fileInput = $('#image');
    if (fileInput) fileInput.click();
  }
  
  // Escape to clear file
  if (e.key === 'Escape' && currentFile) {
    clearFile();
  }
  
  // Ctrl/Cmd + Enter to submit form
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const predictBtn = $('#predictBtn');
    if (predictBtn && !predictBtn.disabled) {
      predictBtn.click();
    }
  }
});

// Smooth scroll for navigation links
$$('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = $(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Initialize tooltips
$$('[data-bs-toggle="tooltip"]').forEach(el => {
  new bootstrap.Tooltip(el);
});

// Page load animations
window.addEventListener('load', () => {
  // Animate elements on page load
  $$('.animate__animated').forEach((el, index) => {
    setTimeout(() => {
      el.style.animationDelay = `${index * 0.1}s`;
    }, 100);
  });
  
  // Show welcome message
  const hasVisited = localStorage.getItem('fruit-ai-visited');
  if (!hasVisited) {
    setTimeout(() => {
      showToast('Welcome to Fruit Quality AI! Upload an image to get started.', 'info');
      localStorage.setItem('fruit-ai-visited', 'true');
    }, 2000);
  }
});

// Performance monitoring
const performanceMonitor = {
  startTime: Date.now(),
  
  logPerformance: () => {
    const loadTime = Date.now() - performanceMonitor.startTime;
    console.log(`Page loaded in ${loadTime}ms`);
  },
  
  trackUserInteraction: (action) => {
    console.log(`User action: ${action} at ${new Date().toISOString()}`);
  }
};

// Track page load performance
window.addEventListener('load', performanceMonitor.logPerformance);

// Track file interactions
const fileInput = $('#image');
if (fileInput) {
  fileInput.addEventListener('change', () => {
    performanceMonitor.trackUserInteraction('file_selected');
  });
}

// Error handling
window.addEventListener('error', (e) => {
  console.error('JavaScript error:', e.error);
  showToast('An unexpected error occurred. Please refresh the page.', 'danger');
});

// Service Worker registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('SW registered: ', registration);
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Export functions for global access
window.FruitAI = {
  clearFile,
  showInvalidImage,
  clearInvalidImage,
  showToast,
  validateFile,
  isProcessing: () => isProcessing
};
