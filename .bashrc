alias ls='ls --color=auto'

#プロンプトの設定
# 出力の後に改行を入れる
function add_line {
  if [[ -z "${PS1_NEWLINE_LOGIN}" ]]; then
  PS1_NEWLINE_LOGIN=true
  else
  printf '\n'
  fi
}
PROMPT_COMMAND='add_line'

export PS1='\[\e[37;45m\] \h \[\e[35;47m\]\[\e[30;47m\] \w \[\e[37;46m\]\[\e[30m\] \[\e[36;49m\]\[\e[0m\]\n > '
