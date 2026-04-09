from PIL import Image

# Load collage image
img = Image.open("static/img/collage.png")

w, h = img.size

# Split into parts
hero = img.crop((0, 0, w, h * 0.42))
dish1 = img.crop((0, h * 0.42, w / 2, h * 0.72))
dish2 = img.crop((w / 2, h * 0.42, w, h * 0.72))
dish3 = img.crop((w / 2, h * 0.72, w, h))

# Save results
hero.save("static/img/hero.jpg")
dish1.save("static/img/dish1.jpg")
dish2.save("static/img/dish2.jpg")
dish3.save("static/img/dish3.jpg")

print("✅ Images saved successfully!")
