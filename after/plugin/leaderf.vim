" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "openbrowser",
            \   "help": "navigate the openbrowser url",
            \   "manager_id": "leaderf#OpenBrowser#managerId",
            \   "arguments": [
            \   ]
            \ }

" In order that `Leaderf ghq` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=0 LeaderfOpenBrowser Leaderf openbrowser

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfOpenBrowser", "navigate the openbrowser url")
