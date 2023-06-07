

(() => {
    'use strict'
  
    // --------
    // Tooltips
    // --------
    // Instantiate all tooltips in a docs or StackBlitz page
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
      .forEach(tooltip => {
        new bootstrap.Tooltip(tooltip)
      })
  
    // --------
    // Popovers
    // --------
    // Instantiate all popovers in a docs or StackBlitz page
    document.querySelectorAll('[data-bs-toggle="popover"]')
      .forEach(popover => {
        new bootstrap.Popover(popover)
      })

    // $(function(){
    //   // Enables popover
    //   $("[data-toggle=popover]").popover();
    // });
  
    // -------------------------------
    // Toasts
    // -------------------------------
    // Used by 'Placement' example in docs or StackBlitz
    const toastPlacement = document.getElementById('toastPlacement')
    if (toastPlacement) {
      document.getElementById('selectToastPlacement').addEventListener('change', function () {
        if (!toastPlacement.dataset.originalClass) {
          toastPlacement.dataset.originalClass = toastPlacement.className
        }
  
        toastPlacement.className = `${toastPlacement.dataset.originalClass} ${this.value}`
      })
    }
  
    // Instantiate all toasts in a docs page only
    document.querySelectorAll('.bd-example .toast')
      .forEach(toastNode => {
        const toast = new bootstrap.Toast(toastNode, {
          autohide: false
        })
  
        toast.show()
      })
  
    // Instantiate all toasts in a docs page only
    const toastTrigger = document.getElementById('liveToastBtn')
    const toastLiveExample = document.getElementById('liveToast')
    if (toastTrigger) {
      toastTrigger.addEventListener('click', () => {
        const toast = new bootstrap.Toast(toastLiveExample)
  
        toast.show()
      })
    }
  
    // -------------------------------
    // Alerts
    // -------------------------------
    // Used in 'Show live toast' example in docs or StackBlitz
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
    const alertTrigger = document.getElementById('liveAlertBtn')
  
    const appendAlert = (message, type) => {
      const wrapper = document.createElement('div')
      wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
      ].join('')
  
      alertPlaceholder.append(wrapper)
    }
  
    if (alertTrigger) {
      alertTrigger.addEventListener('click', () => {
        appendAlert('Nice, you triggered this alert message!', 'success')
      })
    }
  
    // --------
    // Carousels
    // --------
    // Instantiate all non-autoplaying carousels in a docs or StackBlitz page
    document.querySelectorAll('.carousel:not([data-bs-ride="carousel"])')
      .forEach(carousel => {
        bootstrap.Carousel.getOrCreateInstance(carousel)
      })
  
    // -------------------------------
    // Checks & Radios
    // -------------------------------
    // Indeterminate checkbox example in docs and StackBlitz
    document.querySelectorAll('.bd-example-indeterminate [type="checkbox"]')
      .forEach(checkbox => {
        if (checkbox.id.includes('Indeterminate')) {
          checkbox.indeterminate = true
        }
      })
  
    // -------------------------------
    // Links
    // -------------------------------
    // Disable empty links in docs examples only
    document.querySelectorAll('.bd-content [href="#"]')
      .forEach(link => {
        link.addEventListener('click', event => {
          event.preventDefault()
        })
      })
  
    // -------------------------------
    // Modal
    // -------------------------------
    // Modal 'Varying modal content' example in docs and StackBlitz
    const exampleModal = document.getElementById('exampleModal')
    if (exampleModal) {
      exampleModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget
        // Extract info from data-bs-* attributes
        const recipient = button.getAttribute('data-bs-whatever')
  
        // Update the modal's content.
        const modalTitle = exampleModal.querySelector('.modal-title')
        const modalBodyInput = exampleModal.querySelector('.modal-body input')
  
        modalTitle.textContent = `New message to ${recipient}`
        modalBodyInput.value = recipient
      })
    }
  
    // -------------------------------
    // Offcanvas
    // -------------------------------
    // 'Offcanvas components' example in docs only
    const myOffcanvas = document.querySelectorAll('.bd-example-offcanvas .offcanvas')
    if (myOffcanvas) {
      myOffcanvas.forEach(offcanvas => {
        offcanvas.addEventListener('show.bs.offcanvas', event => {
          event.preventDefault()
        }, false)
      })
    }
  })()
  

    // -------------------------------
    // Tabs
    // -------------------------------
    // '

    const triggerTabList = document.querySelectorAll('#myTab button')
triggerTabList.forEach(triggerEl => {
  const tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', event => {
    event.preventDefault()
    tabTrigger.show()
  })
  })

  const triggerEl = document.querySelector('#myTab button[data-bs-target="#profile"]')
  bootstrap.Tab.getInstance(triggerEl).show() // Select tab by name

  const triggerFirstTabEl = document.querySelector('#myTab li:first-child button')
  bootstrap.Tab.getInstance(triggerFirstTabEl).show() // Select first tab
