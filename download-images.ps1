$webClient = New-Object System.Net.WebClient

# Create images directory if it doesn't exist
$imageDir = "public/images/products"
if (-not (Test-Path -Path $imageDir)) {
    New-Item -ItemType Directory -Path $imageDir -Force
}

# Download honey image
$webClient.DownloadFile(
    "https://images.unsplash.com/photo-1551218808-94e208a2daf7?w=800&auto=format&fit=crop&q=80",
    "$imageDir/honey.jpg"
)

# Download shea butter image
$webClient.DownloadFile(
    "https://images.unsplash.com/photo-1600857774236-5a9bcf7efb50?w=800&auto=format&fit=crop&q=80",
    "$imageDir/shea-butter.jpg"
)

# Download argan oil image
$webClient.DownloadFile(
    "https://images.unsplash.com/photo-1631729371254-42c2892fbeca?w=800&auto=format&fit=crop&q=80",
    "$imageDir/argan-oil.jpg"
)

Write-Host "Images downloaded successfully to $imageDir"
