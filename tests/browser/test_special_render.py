"""Real rasterization/indicator checks using an isolated, non-shipped view harness."""
def fixture():
    return {'status':'running','board':[[None]*10 for _ in range(20)],'piece':{'kind':'T','rotation':0,'x':3,'y':0},'queue':['I'],'penetrator':False,'bonuses':0}
def render(page,render_url,state):
    page.goto(render_url)
    page.evaluate('(s)=>window.renderFixture(s)',state)
def pixel(page,x,y):
    return page.locator('#board').evaluate('(c,p)=>Array.from(c.getContext("2d").getImageData(Math.floor((p[0]+.5)*c.width/10),Math.floor((p[1]+.5)*c.height/20),1,1).data)',[x,y])
def test_dynamic_ghost_hidden_above_midline_and_shown_below(page,render_url):
    s=fixture();s['board'][9]=['J']*10
    render(page,render_url,s)
    assert pixel(page,4,8)==[17,26,40,255]
    assert pixel(page,4,9)==[99,142,232,255]
    s=fixture();render(page,render_url,s)
    assert pixel(page,4,19)!=[17,26,40,255]

def test_white_penetrator_and_bonus_symbols(page,render_url):
    s=fixture();s['penetrator']=True;s['bonuses']=3;s['board'][10][4]='J';s['board'][19][9]='P'
    render(page,render_url,s)
    assert pixel(page,4,0)==[255,255,255,255]
    assert pixel(page,9,19)==[255,255,255,255]
    assert pixel(page,4,19)!=[17,26,40,255]
    assert page.locator('#bonuses').text_content()=='\u26a1'*3
    s['bonuses']=1;render(page,render_url,s)
    assert page.locator('#bonuses').text_content()=='\u26a1'
    s['bonuses']=0;render(page,render_url,s)
    assert page.locator('#bonuses').text_content()==''
