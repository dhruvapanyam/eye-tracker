canvas = document.getElementById('grid')
canvas.style,marginLeft = '0%'
canvas.style,marginTop = '0%'
canvas.width = window.innerWidth
canvas.height = window.innerHeight

window.addEventListener('resize',e => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
})

GRID_SIZE = 3

ctx = canvas.getContext('2d')

function drawGrid(n=GRID_SIZE){
    ctx.strokeStyle = '#888888'
    ctx.beginPath()
    for (let i=0;i<n;i++){
        ctx.moveTo(i*canvas.width/n, 0)
        ctx.lineTo(i*canvas.width/n,canvas.height)
    }
    for (let i=0;i<n;i++){
        ctx.moveTo(0,i*canvas.height/n)
        ctx.lineTo(canvas.width,i*canvas.height/n)
    }
    ctx.stroke()
}

mouseX = 0
mouseY = 0

mrow = 0
mcol = 0

arow = null
acol = null

document.addEventListener('mousemove', e => {
    mouseX = e.clientX
    mouseY = e.clientY
    mrow = parseInt(mouseY / (canvas.height / GRID_SIZE))
    mcol = parseInt(mouseX / (canvas.width / GRID_SIZE))
})

function fillMouseBox(n=GRID_SIZE){
    

    // console.log(mouseX,mouseY)
    // console.log(col*canvas.width/n, row*canvas.width/n, canvas.width/n, canvas.height/n)
    // console.log(row,col)

    let w = canvas.width/n
    let h = canvas.height/n

    

    if (arow!=null && acol!=null){
        if(arow == mrow && acol == mcol){
            ctx.fillStyle = '#5ec46c'
            ctx.fillRect(acol*w, arow*h, w, h)
        }
        else{
            ctx.fillStyle = '#db6565'
            ctx.fillRect(acol*w, arow*h, w, h)
            ctx.fillStyle = '#63c5d6'
            ctx.fillRect(mcol*w, mrow*h, w, h)
        }
    }
    else{
        ctx.fillStyle = '#63c5d6'
        ctx.fillRect(mcol*w, mrow*h, w, h)
            
    }
}

function animate(){

    ctx.fillStyle = '#efefef'
    ctx.globalAlpha = 1
    ctx.fillRect(0,0,canvas.width,canvas.height)
    drawGrid()
    fillMouseBox()
    requestAnimationFrame(animate)
    
}

animate()


document.addEventListener('keydown', function(k) {
    k = k.key
    if (k == ' '){
        arow = parseInt(Math.random() * GRID_SIZE)
        acol = parseInt(Math.random() * GRID_SIZE)
        console.log(arow,acol)
    }
    if (k >= '1' && k <= '9'){
        GRID_SIZE = parseInt(k)
    }
})