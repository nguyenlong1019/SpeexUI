class Slider {
    constructor(root, options = {}) {
        // DOM
        this.root = root;
        this.track = root.querySelector('[data-slider-track]');
        this.slides = [...this.track.children];
        this.prevBtn = root.querySelector('[data-slider-prev]');
        this.nextBtn = root.querySelector('[data-slider-next]');
        this.dotsWrapper = root.querySelector('[data-slider-dots]');

        // Options
        const defaults = {
            slidesToShow: {
                default: 1,
                768: 2,
                992: 3,
                1140: 4
            },
            loop: true,
            autoplay: false,
            interval: 5000,
            gap: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--slider-gap')),
        };
        this.opts = {...defaults, ...options};

        // State
        this.currentIndex = 0;
        this.timer = null;

        // Build 
        this.#setup();
        this.#createDots();
        this.#update();
        this.#attachEvents();
    }

    #setup() {
        // compute slide with per breakpoint 
        this.#computePerView();
        window.addEventListener('resize', () => {
            this.#computePerView();
            this.#update();
        });
    }

    #computePerView() {
        const width = window.innerWidth;
        const breakpoints = Object.keys(this.opts.slidesToShow)
        .filter((bp) => bp !== 'default')
        .map(Number)
        .sort((a, b) => a - b);

        let perView = this.opts.slidesToShow.default;
        breakpoints.forEach((bp) => {
            if (width >= bp) perView = this.opts.slidesToShow[bp];
        });

        this.perView = perView;
        const totalGap = this.opts.gap * (perView - 1);
        const slideWidth = (this.root.clientWidth - totalGap - (parseInt(getComputedStyle(this.root).paddingLeft) + parseInt(getComputedStyle(this.root).paddingRight))) / perView;
        this.slideWidth = slideWidth;
        this.slides.forEach((s) => (s.style.width = `${slideWidth}px`));
    }

    #createDots() {
        this.dotsWrapper.innerHTML = '';
        this.dots = this.slides.map((_, i) => {
            const dot = document.createElement('span');
            dot.className = 'slider-dot';
            dot.addEventListener('click', () => this.goTo(i));
            this.dotsWrapper.appendChild(dot);
            return dot;
        });
    }

    #update() {
        const offset = (this.slideWidth + this.opts.gap) * this.currentIndex;
        this.track.style.transform = `translateX(-${offset}px)`;
        this.dots.forEach((d, i) => d.classList.toggle('active', i === this.currentIndex));
    }

    #attachEvents() {
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());
        if (this.opts.autoplay) {
            this.root.addEventListener('mouseenter', () => this.#pause());
            this.root.addEventListener('mouseleave', () => this.#play());
            this.#play();
        }
    }

    #play() {
        this.timer = setInterval(() => this.next(), this.opts.interval);
    }

    #pause() {
        clearInterval(this.timer);
    }

    next() {
        if (this.currentIndex < this.slides.length - this.perView) {
            this.currentIndex++;
        } else if (this.opts.loop) {
            this.currentIndex = 0;
        }
        this.#update();
    }

    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
        } else if (this.opts.loop) {
            this.currentIndex = this.slides.length - this.perView;
        }
        this.#update();
    }

    goTo(index) {
        if (index >= 0 && index <= this.slides.length - this.perView) {
            this.currentIndex = index;
            this.#update();
        }
    }
}