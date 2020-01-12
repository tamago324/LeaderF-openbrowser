" ============================================================================
" File:        OpenBrowser.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from openbrowserExpl import *"

function! leaderf#OpenBrowser#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "openbrowserExplManager.accept()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "openbrowserExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "openbrowserExplManager.accept()"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "openbrowserExplManager.quit()"<CR>
    nnoremap <buffer> <silent> <Tab>         :exec g:Lf_py "openbrowserExplManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "openbrowserExplManager.toggleHelp()"<CR>
    if has_key(g:Lf_NormalMap, "OpenBrowser")
        for i in g:Lf_NormalMap["OpenBrowser"]
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction

function! leaderf#OpenBrowser#managerId()
    " pyxeval() has bug
    if g:Lf_PythonVersion == 2
        return pyeval("id(openbrowserExplManager)")
    else
        return py3eval("id(openbrowserExplManager)")
    endif
endfunction
