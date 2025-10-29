// XYD Embed Enhancement
document.addEventListener('DOMContentLoaded', function() {
  const embedContainers = document.querySelectorAll('.xyd-embed-container');
  
  embedContainers.forEach(container => {
    const iframe = container.querySelector('iframe');
    const loading = container.querySelector('.xyd-embed-loading');
    
    if (iframe && loading) {
      // Hide loading when iframe loads
      iframe.addEventListener('load', function() {
        setTimeout(() => {
          loading.classList.add('hidden');
        }, 500);
      });
      
      // Handle iframe load errors
      iframe.addEventListener('error', function() {
        loading.innerHTML = `
          <div class="xyd-embed-fallback">
            <p>Failed to load documentation.</p>
            <a href="${iframe.src}" target="_blank" class="xyd-embed-fallback-link">
              Open in new window →
            </a>
          </div>
        `;
      });
    }
  });
  
  // Handle responsive behavior
  function handleResize() {
    const mobileBreakpoint = 768;
    const responsiveEmbeds = document.querySelectorAll('.xyd-embed-container[data-responsive="true"] iframe');
    
    responsiveEmbeds.forEach(iframe => {
      if (window.innerWidth <= mobileBreakpoint) {
        iframe.style.height = '500px';
      }
    });
  }
  
  window.addEventListener('resize', handleResize);
  handleResize(); // Initial call
});
