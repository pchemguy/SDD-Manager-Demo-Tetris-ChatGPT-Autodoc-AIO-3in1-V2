"""Geometry contracts use real DOM/text at required widths and doubled text scale."""
import pytest

def geometry(page):
    return page.evaluate("""() => {const selectors=['#leaderboard','.info','#board','#settings','#help'];return Object.fromEntries(selectors.map(s=>{const r=document.querySelector(s).getBoundingClientRect();return [s,{hidden:document.querySelector(s).hidden,left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width}]}))}""")

def assert_center_and_order(page,width):
    page.wait_for_function("Math.abs((document.querySelector('#board').getBoundingClientRect().left+document.querySelector('#board').getBoundingClientRect().right)/2-innerWidth/2)<1")
    boxes=geometry(page);order=[s for s in ['#leaderboard','.info','#board','#settings','#help'] if not boxes[s]['hidden']]
    for left,right in zip(order,order[1:]):assert boxes[left]['right']<=boxes[right]['left']+1
    assert boxes['.info']['left']>=-1 and boxes['.info']['right']<=width
    assert boxes['#board']['left']>=-1 and boxes['#board']['right']<=width

def text_overflow(page):
    return page.evaluate("""() => {const errors=[];for(const panel of document.querySelectorAll('.panel')){if(panel.hidden)continue;const bounds=panel.getBoundingClientRect(),walk=document.createTreeWalker(panel,NodeFilter.SHOW_TEXT);let node;while(node=walk.nextNode()){if(!node.textContent.trim()||node.parentElement.closest('select,option'))continue;const range=document.createRange();range.selectNodeContents(node);for(const r of range.getClientRects())if(r.width&&(r.left<bounds.left-1||r.right>bounds.right+1))errors.push(node.textContent);}}return errors;}""")

@pytest.mark.parametrize('width',[640,960,1280,1600,1920])
def test_centered_ordered_workspace_at_default_and_double_text(page,width):
    page.set_viewport_size(dict(width=width,height=1200))
    for scale in [14,28]:
        page.evaluate('(scale)=>document.documentElement.style.fontSize=scale+"px"',scale)
        assert_center_and_order(page,width)
        assert text_overflow(page)==[]

@pytest.mark.parametrize('width',[640,960,1280,1600,1920])
def test_all_visibility_combinations_with_full_scores_and_text_scaling(page,width):
    import json,itertools,os
    from pathlib import Path
    from test_panels import select_panels
    from test_files import restore,observable
    from test_file_validation import full_candidate
    from playwright.sync_api import expect
    page.set_viewport_size(dict(width=width,height=1200))
    restore(page,json.dumps(full_candidate()).encode());expect(page.locator('#notice')).to_contain_text('Restored')
    before=observable(page)
    for scale in [14,28]:
        page.evaluate('(scale)=>document.documentElement.style.fontSize=scale+"px"',scale)
        for visible in itertools.product([False,True],repeat=3):
            select_panels(page,visible);assert_center_and_order(page,width)
            assert text_overflow(page)==[]
            assert observable(page)==before
        if width in [640,1920]:
            page.evaluate('window.scrollTo(0,0)');Path('test-results').mkdir(exist_ok=True)
            page.screenshot(path=f"test-results/layout-{os.environ.get('TETRIS_BROWSER','chromium')}-{width}-{scale}.png")
