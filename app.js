// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in (optional for basic map, required for location)
    function checkAuth() {
        const token = localStorage.getItem('token');
        return !!token;
    }

    // Show login prompt if not authenticated (but don't block map)
    if (!checkAuth()) {
        const userInfo = document.getElementById('user-info');
        if (userInfo) {
            userInfo.innerHTML = '<a href="login.html" style="color: white; text-decoration: none;">Login</a>';
        }
    }

    // Initialize map centered on Cagayan de Oro
    const map = L.map('map').setView([8.483, 124.648], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    let establishments = [];
    let markers = [];
    let userLocation = null;
    let userMarker = null;
    let watchId = null; // For real-time location tracking
    
    // Use environment variable in production, fallback to localhost for development
    const API_BASE = (typeof window !== 'undefined' && window.location.hostname !== 'localhost') 
        ? `${window.location.protocol}//${window.location.host}/api`
        : 'http://localhost:5000/api';

    // Display user info if logged in
    if (checkAuth()) {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const userNameEl = document.getElementById('user-name');
        if (userNameEl && user.name) {
            userNameEl.textContent = `👤 ${user.name}`;
        }
        
        // Logout functionality
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.reload();
            });
        }
    }

    // Get auth headers (optional)
    function getAuthHeaders() {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    // Load establishments from backend
    async function loadEstablishments() {
        try {
            const response = await fetch(`${API_BASE}/establishments`, {
                headers: getAuthHeaders()
            });
            if (!response.ok) {
                if (response.status === 401) {
                    // If unauthorized, just clear token but don't redirect
                    localStorage.removeItem('token');
                    console.log('Not authenticated. Map will work but location features require login.');
                }
                throw new Error('Failed to load establishments');
            }
            establishments = await response.json();
            displayListings(establishments);
            addMarkers(establishments);
        } catch (error) {
            console.error('Error loading establishments:', error);
            console.log('Backend might not be running. Map will still work for exploration.');
            // Show message in listings
            const listings = document.getElementById('listings');
            if (listings) {
                listings.innerHTML = '<li style="text-align: center; color: #999; padding: 20px;">Backend server not running. Please start the backend to see places.</li>';
            }
        }
    }

    // Display listings in sidebar
    function displayListings(list) {
        const listings = document.getElementById('listings');
        if (!listings) return;
        
        listings.innerHTML = '';
        
        if (list.length === 0) {
            listings.innerHTML = '<li style="text-align: center; color: #999;">No places found</li>';
            return;
        }
        
        list.forEach(est => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>${est.name}</strong>
                <span class="category">${est.category || est.type}</span>
                <div class="rating">${'★'.repeat(Math.floor(est.rating || 0))} ${(est.rating || 0).toFixed(1)}/5</div>
                <div class="description">${est.description || est.address || ''}</div>
            `;
            li.addEventListener('click', () => {
                map.setView([est.lat || est.latitude, est.lng || est.longitude], 15);
                highlightPlace(est);
            });
            listings.appendChild(li);
        });
    }

    // Add markers to map
    function addMarkers(list) {
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];
        
        list.forEach(est => {
            const lat = est.lat || est.latitude;
            const lng = est.lng || est.longitude;
            const category = est.category || est.type;
            
            if (!lat || !lng) return; // Skip if no coordinates
            
            // Different colors for different categories
            let iconColor = '#667eea';
            if (category === 'Mall') iconColor = '#e74c3c';
            else if (category === 'Restaurant') iconColor = '#f39c12';
            else if (category === 'Landmark') iconColor = '#3498db';
            else if (category === 'Dorm/Hotel') iconColor = '#9b59b6';
            
            const customIcon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${iconColor}; width: 25px; height: 25px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
                iconSize: [25, 25],
                iconAnchor: [12, 12]
            });
            
            const marker = L.marker([lat, lng], { icon: customIcon })
                .addTo(map)
                .bindPopup(`<b>${est.name}</b><br>${est.description || est.address || ''}`);
            markers.push(marker);
        });
    }

    // Highlight a specific place
    function highlightPlace(est) {
        markers.forEach(marker => {
            marker.setOpacity(0.5);
        });
        
        const lat = est.lat || est.latitude;
        const lng = est.lng || est.longitude;
        
        const highlightMarker = L.marker([lat, lng])
            .addTo(map)
            .bindPopup(`<b>${est.name}</b><br>${est.description || est.address || ''}`)
            .openPopup();
        
        setTimeout(() => {
            markers.forEach(marker => marker.setOpacity(1));
            map.removeLayer(highlightMarker);
        }, 3000);
    }

    // Update user location on map (real-time)
    function updateUserLocation(lat, lng) {
        userLocation = { lat, lng };
        
        // Remove old marker
        if (userMarker) {
            map.removeLayer(userMarker);
        }
        
        // Create pulsing user location marker
        const userIcon = L.divIcon({
            className: 'user-location-marker',
            html: '<div class="user-location-marker pulse"></div>',
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });
        
        userMarker = L.marker([lat, lng], { 
            icon: userIcon,
            zIndexOffset: 1000 // Always on top
        }).addTo(map);
        
        // Update map view smoothly
        map.setView([lat, lng], 14, { animate: true, duration: 0.5 });
    }

    // Get user's location with real-time tracking
    async function getLocation() {
        // Require login for location features
        if (!checkAuth()) {
            if (confirm('Please login to use location features. Go to login page?')) {
                window.location.href = 'login.html';
            }
            return;
        }
        
        if (!navigator.geolocation) {
            alert('Geolocation is not supported by your browser.');
            return;
        }
        
        const locateBtn = document.getElementById('locate-me');
        if (!locateBtn) return;
        
        // If already tracking, stop it
        if (watchId !== null) {
            navigator.geolocation.clearWatch(watchId);
            watchId = null;
            locateBtn.textContent = '📍 Locate Me';
            locateBtn.style.background = '';
            if (userMarker) {
                map.removeLayer(userMarker);
                userMarker = null;
            }
            return;
        }
        
        locateBtn.textContent = '📍 Tracking...';
        locateBtn.style.background = '#4CAF50';
        locateBtn.disabled = false;
        
        // Get initial position
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                updateUserLocation(lat, lng);
                
                // Get address from backend
                try {
                    const response = await fetch(`${API_BASE}/geocode?lat=${lat}&lng=${lng}`, {
                        headers: getAuthHeaders()
                    });
                    const data = await response.json();
                    const address = data.address || `Latitude: ${lat.toFixed(6)}, Longitude: ${lng.toFixed(6)}`;
                    
                    // Show location modal
                    showLocationModal(address);
                    
                    // Load nearby places
                    loadNearbyPlaces(lat, lng);
                } catch (error) {
                    console.error('Error getting address:', error);
                    showLocationModal(`Your location: ${lat.toFixed(6)}, ${lng.toFixed(6)}`);
                    loadNearbyPlaces(lat, lng);
                }
                
                // Start watching position for real-time updates
                watchId = navigator.geolocation.watchPosition(
                    (position) => {
                        const newLat = position.coords.latitude;
                        const newLng = position.coords.longitude;
                        
                        // Only update if location changed significantly (more than 10 meters)
                        if (userLocation) {
                            const distance = calculateDistance(
                                userLocation.lat, userLocation.lng,
                                newLat, newLng
                            );
                            if (distance > 10) { // 10 meters threshold
                                updateUserLocation(newLat, newLng);
                                loadNearbyPlaces(newLat, newLng);
                            }
                        } else {
                            updateUserLocation(newLat, newLng);
                            loadNearbyPlaces(newLat, newLng);
                        }
                    },
                    (error) => {
                        console.error('Error watching position:', error);
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 5000,
                        maximumAge: 0 // Always get fresh position
                    }
                );
            },
            (error) => {
                alert('Error getting location. Please allow location access and make sure you have a GPS signal.');
                locateBtn.textContent = '📍 Locate Me';
                locateBtn.style.background = '';
                locateBtn.disabled = false;
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    }

    // Calculate distance between two coordinates (Haversine formula)
    function calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371000; // Earth radius in meters
        const phi1 = lat1 * Math.PI / 180;
        const phi2 = lat2 * Math.PI / 180;
        const deltaPhi = (lat2 - lat1) * Math.PI / 180;
        const deltaLambda = (lon2 - lon1) * Math.PI / 180;
        
        const a = Math.sin(deltaPhi/2) * Math.sin(deltaPhi/2) +
                  Math.cos(phi1) * Math.cos(phi2) *
                  Math.sin(deltaLambda/2) * Math.sin(deltaLambda/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        
        return R * c; // Distance in meters
    }

    // Show location modal
    function showLocationModal(address) {
        const modal = document.getElementById('location-modal');
        const locationText = document.getElementById('location-text');
        if (modal && locationText) {
            locationText.textContent = `Your location is: ${address}`;
            modal.style.display = 'block';
        }
    }

    // Close modal
    const closeBtn = document.querySelector('.close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            const modal = document.getElementById('location-modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    }

    window.addEventListener('click', (event) => {
        const modal = document.getElementById('location-modal');
        if (event.target === modal && modal) {
            modal.style.display = 'none';
        }
    });

    // Load nearby places
    async function loadNearbyPlaces(lat, lng) {
        try {
            const response = await fetch(`${API_BASE}/nearby?lat=${lat}&lng=${lng}&radius=5000`, {
                headers: getAuthHeaders()
            });
            const nearby = await response.json();
            
            if (nearby.length > 0) {
                displayListings(nearby);
                addMarkers(nearby);
            }
        } catch (error) {
            console.error('Error loading nearby places:', error);
        }
    }

    // Search functionality
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const categoryFilter = document.getElementById('filter')?.value || '';
            
            if (query === '' && categoryFilter === '') {
                displayListings(establishments);
                addMarkers(establishments);
                return;
            }
            
            let filtered = establishments;
            
            // Filter by category
            if (categoryFilter) {
                filtered = filtered.filter(est => {
                    const cat = est.category || est.type;
                    return cat === categoryFilter;
                });
            }
            
            // Filter by search query
            if (query) {
                filtered = filtered.filter(est => {
                    const name = (est.name || '').toLowerCase();
                    const desc = (est.description || '').toLowerCase();
                    const addr = (est.address || '').toLowerCase();
                    const cat = (est.category || est.type || '').toLowerCase();
                    return name.includes(query) || desc.includes(query) || addr.includes(query) || cat.includes(query);
                });
            }
            
            displayListings(filtered);
            addMarkers(filtered);
        });
    }

    // Category filter
    const filterSelect = document.getElementById('filter');
    if (filterSelect) {
        filterSelect.addEventListener('change', (e) => {
            const category = e.target.value;
            const searchQuery = document.getElementById('search')?.value.toLowerCase().trim() || '';
            
            let filtered = establishments;
            
            if (category) {
                filtered = filtered.filter(est => {
                    const cat = est.category || est.type;
                    return cat === category;
                });
            }
            
            if (searchQuery) {
                filtered = filtered.filter(est => {
                    const name = (est.name || '').toLowerCase();
                    const desc = (est.description || '').toLowerCase();
                    const addr = (est.address || '').toLowerCase();
                    return name.includes(searchQuery) || desc.includes(searchQuery) || addr.includes(searchQuery);
                });
            }
            
            displayListings(filtered);
            addMarkers(filtered);
        });
    }

    // Locate me button
    const locateBtn = document.getElementById('locate-me');
    if (locateBtn) {
        locateBtn.addEventListener('click', getLocation);
    }

    // Load establishments on page load
    loadEstablishments();
});
