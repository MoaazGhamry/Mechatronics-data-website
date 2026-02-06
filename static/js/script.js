// Theme Logic (Persistent)
const themeToggle = document.getElementById('themeToggle');
const sunIcon = document.getElementById('sunIcon');
const moonIcon = document.getElementById('moonIcon');

function updateThemeIcons(isDark) {
    if (!sunIcon || !moonIcon) return;
    sunIcon.classList.toggle('hidden', !isDark);
    moonIcon.classList.toggle('hidden', isDark);
}

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        const isDark = document.documentElement.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        updateThemeIcons(isDark);
    });
}

// Initialize Theme Icons
const isDarkMode = document.documentElement.classList.contains('dark');
updateThemeIcons(isDarkMode);


// Slider Logic (Home Page Only)
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const slider = document.getElementById('slider');

if (prevBtn && nextBtn && slider) {
    let scrollAmount = 0;
    const scrollStep = 300;

    nextBtn.addEventListener('click', () => {
        slider.scrollBy({ left: scrollStep, behavior: 'smooth' });
    });

    prevBtn.addEventListener('click', () => {
        slider.scrollBy({ left: -scrollStep, behavior: 'smooth' });
    });
}


// Level Detail Logic (Detail Page Only)
window.showSemester = (num) => {
    const s1 = document.getElementById('semester1');
    const s2 = document.getElementById('semester2');
    const b1 = document.getElementById('sem1Btn');
    const b2 = document.getElementById('sem2Btn');
    const bg = document.getElementById('toggle-bg');

    if (num === 1) {
        if (s1) s1.classList.remove('hidden');
        if (s2) s2.classList.add('hidden');
        if (bg) bg.style.transform = 'translateX(0)';
        if (b1) {
            b1.classList.remove('text-gray-500', 'dark:text-gray-400');
            b1.classList.add('text-forest-green', 'dark:text-white');
        }
        if (b2) {
            b2.classList.remove('text-forest-green', 'dark:text-white');
            b2.classList.add('text-gray-500', 'dark:text-gray-400');
        }
    } else {
        if (s1) s1.classList.add('hidden');
        if (s2) s2.classList.remove('hidden');
        if (bg) bg.style.transform = 'translateX(calc(100% + 0.375rem))';
        if (b2) {
            b2.classList.remove('text-gray-500', 'dark:text-gray-400');
            b2.classList.add('text-forest-green', 'dark:text-white');
        }
        if (b1) {
            b1.classList.remove('text-forest-green', 'dark:text-white');
            b1.classList.add('text-gray-500', 'dark:text-gray-400');
        }
    }
};

window.toggleSubjectCard = (id) => {
    const card = document.getElementById(`card-${id}`);
    const content = document.getElementById(`content-${id}`);
    const wrapper = card ? card.closest('.w-full') : null;
    const parent = card ? card.closest('[id^="semester"]') : null;

    if (!card || !content || !wrapper) {
        console.warn("Could not find components for subject:", id);
        return;
    }

    const isOpen = card.classList.contains('is-open');

    // Close all other open cards in the same container (Accordion behavior)
    if (!isOpen && parent) {
        parent.querySelectorAll('.subject-card.is-open').forEach(otherCard => {
            const otherId = otherCard.id.replace('card-', '');
            const otherContent = document.getElementById(`content-${otherId}`);
            const otherWrapper = otherCard.closest('.w-full');

            otherCard.classList.remove('is-open');
            if (otherContent) otherContent.classList.remove('active');
            if (otherWrapper) otherWrapper.classList.remove('md:col-span-2');
        });
    }

    if (isOpen) {
        // Collapse
        card.classList.remove('is-open');
        content.classList.remove('active');
        // Delay removing col-span to allow width/height transition to start
        setTimeout(() => {
            wrapper.classList.remove('md:col-span-2');
        }, 300);
    } else {
        // Expand
        card.classList.add('is-open');
        wrapper.classList.add('md:col-span-2');
        // Tiny delay to allow grid to allocate column space before animating content
        setTimeout(() => {
            content.classList.add('active');
            // Smooth scroll into view after opening starts
            setTimeout(() => {
                card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        }, 50);
    }
};

window.toggleCollapsible = (id) => {
    const content = document.getElementById(`content-${id}`);
    const icon = document.getElementById(`icon-${id}`);

    if (!content) return;

    const card = content.closest('.group.relative');
    const parent = content.closest('[id^="semester"]');
    const cardWrapper = card && card.parentElement.classList.contains('w-full') ? card.parentElement : card;

    if (content.classList.contains('active')) {
        content.classList.remove('active');
        if (icon) icon.style.transform = 'rotate(0deg)';
        if (cardWrapper) cardWrapper.classList.remove('md:row-span-2');
    } else {
        if (parent) {
            parent.querySelectorAll('.collapsible-content.active').forEach(item => {
                item.classList.remove('active');
                const itemId = item.id.replace('content-', '');
                const itemIcon = document.getElementById(`icon-${itemId}`);
                if (itemIcon) itemIcon.style.transform = 'rotate(0deg)';
                const otherCard = item.closest('.group.relative');
                const otherWrapper = otherCard && otherCard.parentElement.classList.contains('w-full') ? otherCard.parentElement : otherCard;
                if (otherWrapper) otherWrapper.classList.remove('md:row-span-2');
            });
        }
        content.classList.add('active');
        if (icon) icon.style.transform = 'rotate(180deg)';
        if (cardWrapper) {
            cardWrapper.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            setTimeout(() => {
                cardWrapper.classList.add('md:row-span-2');
                cardWrapper.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 50);
        }
    }
};
